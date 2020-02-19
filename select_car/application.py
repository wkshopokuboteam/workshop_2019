import wx
import wx.adv
import os
import yaml
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import sqlite3
from select_car import create_db
from select_car import learning
from select_car import progress
import threading
from PIL import Image

default_yaml_filename = "config.yaml"


class FileDropTarget(wx.FileDropTarget):
    """ Drag & Drop Class """

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window
        self.db = window.db

    def OnDropFiles(self, x, y, files):
        self.window.text_entry.SetLabel(files[0])

        message = self.judge(files[0])

        self.window.text_result.SetLabel(message)

        return 0

    # 学習結果に基づいて入力された画像を判定するメソッド
    def judge(self, file):
        # 保存したモデルの読み込み
        model = model_from_json(open('learningresult/car_predict.json').read())
        # 保存した重みの読み込み
        model.load_weights('learningresult/car_predict.hdf5')

        # 画像を読み込む
        img_path = str(file)
        img = image.load_img(img_path, target_size=(150, 150, 3))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        # 予測
        features = model.predict(x)
        print(features)

        # 予測結果によって処理を分ける
        folder = os.listdir("traindata")
        maxindex = np.argmax(features[0])
        car = folder[maxindex]
        print(np.sum(features[0]))
        print(features[0, maxindex])

        message = "選ばれたのは「" + car + "」です。"

        # flag = 0
        # for i in range(0, 10):
        #     if features[0, i] == 1:
        #         id = i
        #         cat = folder[i]
        #         flag = 1
        #     if flag == 1:
        #         message = "選ばれたのは「" + cat + "」です。"
        #     else:
        #         message = "識別できませんでした。"

        return message


class AppTable(wx.ListCtrl):

    def __init__(self, parent, main):
        self.db = main.db
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_HRULES)
        self.InsertColumn(0, "学習データ")
        self.InsertColumn(1, "学習データのバリエーション数")
        self.InsertColumn(2, "学習回数")
        self.refresh()

    def refresh(self):
        # データベースに接続する
        # conn = sqlite3.connect('database/example.db')
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        try:
            c.execute("SELECT name, learning_file_count, learning_count FROM cars")
        except sqlite3.OperationalError:
            create_db.CreateDB().execute()
            c.execute("SELECT name, learning_file_count, learning_count FROM cars")

        data = c.fetchall()
        conn.commit()
        conn.close()
        self.DeleteAllItems()
        for line in range(len(data)):
            self.InsertItem(line, data[line][0])
            self.SetItem(line, 1, str(data[line][1]))
            self.SetItem(line, 2, str(data[line][2]))


class App(wx.Frame):
    """ GUI """

    def __init__(self, parent, id, title):
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + default_yaml_filename, "r",
                  encoding="utf-8") as f:
            y = yaml.load(stream=f, Loader=yaml.SafeLoader)
            self.db = y.get("db").get("path") + y.get("db").get("fileName")
            self.logo = y.get("resource").get("path") + y.get("resource").get("logo")
            self.result = y.get("result")

        wx.Frame.__init__(self, parent, id, title, size=(500, 300), style=wx.DEFAULT_FRAME_STYLE)
        self.progress = progress.ProgressComponent(self)
        # アイコン
        icon = wx.Icon(self.logo, wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        # 各パネルの設定
        notebook = wx.Notebook(self, wx.ID_ANY)
        self.main_panel_setting(notebook)
        self.learning_condition_panel_setting(notebook)
        self.learning_panel_setting(notebook)
        # 表示
        self.Show()

    ###########################################
    # パネル1
    # ドラッグされた画像を判定するパネル
    ###########################################
    def main_panel_setting(self, notebook):
        p = wx.Panel(notebook, wx.ID_ANY)
        label = wx.StaticText(p, wx.ID_ANY, 'ここにファイルをドロップしてください', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        label.SetBackgroundColour("#e0ffff")
        # ドロップ対象の設定
        label.SetDropTarget(FileDropTarget(self))
        # テキスト入力ウィジット
        text_entry = wx.TextCtrl(p, wx.ID_ANY)
        # テキスト入力ウィジット
        text_result = wx.StaticText(p, wx.ID_ANY, '結果をここに出力', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        # レイアウト
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(label, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        layout.Add(text_entry, flag=wx.EXPAND | wx.ALL, border=10)
        layout.Add(text_result, flag=wx.EXPAND | wx.ALL, border=10)
        p.SetSizer(layout)
        notebook.InsertPage(0, p, "Application")

    ###########################################
    # パネル2
    # 学習状況を表示するパネル
    ###########################################
    def learning_condition_panel_setting(self, notebook):
        p = wx.Panel(notebook, wx.ID_ANY)
        layout = wx.BoxSizer(wx.VERTICAL)
        self.app_table = AppTable(p, self)
        self.refresh_button = wx.Button(p, -1, "更新")
        self.Bind(wx.EVT_BUTTON, self.refresh_event, self.refresh_button)
        layout.Add(self.refresh_button, flag=wx.ALL, border=10)
        layout.Add(self.app_table, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        p.SetSizer(layout)
        notebook.InsertPage(1, p, "Learning Condition")

    ###########################################
    # パネル3
    # 学習を行うパネル
    ###########################################
    def learning_panel_setting(self, notebook):
        p = wx.Panel(notebook, wx.ID_ANY)
        layout = wx.BoxSizer(wx.VERTICAL)
        # 学習実施
        self.makeButton = wx.Button(p, -1, "学習を実施", size=(150, 60))
        self.Bind(wx.EVT_BUTTON, self.make_data_event, self.makeButton)
        layout.Add(self.makeButton, flag=wx.ALL, border=10)
        # 学習結果を確認
        self.checkButton = wx.Button(p, -1, "学習結果を確認", size=(150, 60))
        self.Bind(wx.EVT_BUTTON, self.check_result, self.checkButton)
        layout.Add(self.checkButton, flag=wx.ALL, border=10)

        p.SetSizer(layout)
        notebook.InsertPage(2, p, "Learning Maintenance")

    def refresh_event(self, event):
        self.app_table.refresh()

    def make_data_event(self, event):
        self.progress.Show()
        thread = threading.Thread(target=learning.Learning().execute())
        thread.start()
        wait_thread = threading.Thread(target=self.wait_make_data(thread))
        wait_thread.start()

    def wait_make_data(self, thread):
        thread.join()
        self.progress.Destroy()
        dialog = wx.MessageDialog(None, 'データの作成が完了しました。\r\n出力先：' + self.result.get("path"), '確認ダイアログ', wx.OK)
        result = dialog.ShowModal()
        if result == wx.ID_OK:
            dialog.Destroy()

    def check_result(self, event):
        file_name = self.result.get("path") + self.result.get("fit") + ".png"
        try:
            result = Image.open(file_name)
            result.show()
        except FileNotFoundError:
            dialog = wx.MessageDialog(None, 'ファイルがありません。\r\nファイル名：' + file_name, 'Not Found', wx.OK)
            result = dialog.ShowModal()
            if result == wx.ID_OK:
                dialog.Destroy()


app = wx.App()
App(None, -1, 'タイトル')
app.MainLoop()
