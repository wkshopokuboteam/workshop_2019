
import wx
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import sqlite3
import os

class FileDropTarget(wx.FileDropTarget):
    """ Drag & Drop Class """

    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.window = window

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
        img = image.load_img(img_path,target_size=(150, 150, 3))
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

class App(wx.Frame):
    """ GUI """

    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(1000, 200), style=wx.DEFAULT_FRAME_STYLE)

        # パネル
        p = wx.Panel(self, wx.ID_ANY)

        label = wx.StaticText(p, wx.ID_ANY, 'ここにファイルをドロップしてください', style=wx.SIMPLE_BORDER | wx.TE_CENTER)
        label.SetBackgroundColour("#e0ffff")

        # ドロップ対象の設定
        label.SetDropTarget(FileDropTarget(self))

        # テキスト入力ウィジット
        self.text_entry = wx.TextCtrl(p, wx.ID_ANY)
        
        # テキスト入力ウィジット
        self.text_result = wx.StaticText(p, wx.ID_ANY, '結果をここに出力', style=wx.SIMPLE_BORDER | wx.TE_CENTER)

        # レイアウト
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(label, flag=wx.EXPAND | wx.ALL, border=10, proportion=1)
        layout.Add(self.text_entry, flag=wx.EXPAND | wx.ALL, border=10)
        layout.Add(self.text_result, flag=wx.EXPAND | wx.ALL, border=10)
        p.SetSizer(layout)

        self.Show()


app = wx.App()
App(None, -1, 'タイトル')
app.MainLoop()
