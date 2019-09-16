
import wx
from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import sqlite3


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
        model = model_from_json(open('learningresult/tea_predict.json').read())
        # 保存した重みの読み込み
        model.load_weights('learningresult/tea_predict.hdf5')

        categories = ["綾鷹", "おおいお茶", "おおいお茶濃い茶", "伊右衛門", "生茶", "天然水GREENTEA"]

        # 画像を読み込む
        img_path = str(file)
        img = image.load_img(img_path,target_size=(150, 150, 3))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)

        # 予測
        features = model.predict(x)

        # 予測結果によって処理を分ける
        if features[0, 0] == 1:
            selectedcount = self.countup(0)
            message = "選ばれたのは、綾鷹でした。綾鷹は" + str(selectedcount) + "回目"
        elif features[0, 3] == 1:
            selectedcount = self.countup(3)
            message = "選ばれたのは、伊右衛門でした。伊右衛門は" + str(selectedcount) + "回目"
        else:
            flag = 0
            for i in range(0, 6):
                  if features[0, i] == 1:
                      id = i
                      cat = categories[i]
                      flag = 1
            if flag == 1:
                selectedcount = self.countup(id)
                message = "綾鷹を選んでください。（もしかして：あなたが選んでいるのは「" + cat + "」ではありませんか？ " + cat + "は" + str(selectedcount) + "回目）"
            else:
                selectedcount = self.countup(6)
                message = "識別できませんでした。識別不能は" + str(selectedcount) + "回目"
                
        return message
    
    # データベースの選択回数を更新するメソッド
    def countup(self, id):
        # データベースに接続する
        conn = sqlite3.connect('database/example.db')
        c = conn.cursor()
        
        # 更新前の回数を取得する
        c.execute("SELECT count FROM teas WHERE id = ?", (id, ))
        
        # 回数をインクリメントする
        for row in c:
            updatecount = row[0] + 1
        
        # インクリメント後の回数に更新する
        c.execute("UPDATE teas SET count = ? WHERE id = ?", (updatecount, id))
        
        # 更新結果を保存（コミット）する
        conn.commit()
        
        # データベースへのアクセスが終わったら close する
        conn.close()
        
        return updatecount


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
