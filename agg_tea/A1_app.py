import wx

from keras.models import model_from_json
from keras.preprocessing import image
import numpy as np
import sqlite3
import shutil
import glob


# 学習結果に基づいて入力された画像を判定するメソッド
def judge(file):
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
    for i in range(0, 6):
        if features[0, i] == 1:
            cat = categories[i]
            return cat
    cat = "anonymous"
    return cat


# データベースの売上個数を更新するメソッド
def countup(tea, shop):
    # データベースに接続する
    conn = sqlite3.connect('database/example.db')
    c = conn.cursor()
    
    # 更新前の売上個数を取得する
    c.execute("SELECT count FROM teas WHERE tea = ? AND shop = ?", (tea, shop) )
    
    # 売上個数をインクリメントする
    for row in c:
        updatecount = row[0] + 1
    
    # インクリメント後の売上個数に更新する
    c.execute("UPDATE teas SET count = ? WHERE tea = ? AND shop = ?", (updatecount, tea, shop))
    
    # 更新結果を保存（コミット）する
    conn.commit()
    
    # データベースへのアクセスが終わったら close する
    conn.close()


# 各緑茶、店舗の売上個数を取得するメソッド
def select_sold_count(tea, shop):
    # データベースに接続する
    conn = sqlite3.connect('database/example.db')
    c = conn.cursor()

    # 売上個数を取得する
    c.execute("SELECT count FROM teas WHERE tea = ? AND shop = ?", (tea, shop))
    for row in c:
        sold_count = row[0]

    return sold_count

# 各緑茶、店舗の売上個数を表示するメソッド
def display_sold_count():
    grid_result11.SetLabel(str(select_sold_count("綾鷹", "A店")))
    grid_result12.SetLabel(str(select_sold_count("綾鷹", "B店")))
    grid_result13.SetLabel(str(select_sold_count("綾鷹", "C店")))
    grid_result21.SetLabel(str(select_sold_count("おおいお茶", "A店")))
    grid_result22.SetLabel(str(select_sold_count("おおいお茶", "B店")))
    grid_result23.SetLabel(str(select_sold_count("おおいお茶", "C店")))
    grid_result31.SetLabel(str(select_sold_count("おおいお茶濃い茶", "A店")))
    grid_result32.SetLabel(str(select_sold_count("おおいお茶濃い茶", "B店")))
    grid_result33.SetLabel(str(select_sold_count("おおいお茶濃い茶", "C店")))
    grid_result41.SetLabel(str(select_sold_count("伊右衛門", "A店")))
    grid_result42.SetLabel(str(select_sold_count("伊右衛門", "B店")))
    grid_result43.SetLabel(str(select_sold_count("伊右衛門", "C店")))
    grid_result51.SetLabel(str(select_sold_count("生茶", "A店")))
    grid_result52.SetLabel(str(select_sold_count("生茶", "B店")))
    grid_result53.SetLabel(str(select_sold_count("生茶", "C店")))
    grid_result61.SetLabel(str(select_sold_count("天然水GREENTEA", "A店")))
    grid_result62.SetLabel(str(select_sold_count("天然水GREENTEA", "B店")))
    grid_result63.SetLabel(str(select_sold_count("天然水GREENTEA", "C店")))

# 振り分けボタン押下時の処理
def click_button_1(event):

    shops = ["A店", "B店", "C店"]

    for idx, shop in enumerate(shops):
        inputdir = "./inputdata/" + shop
        files = glob.glob(inputdir + "/*.jpg")
        for f in files:
            tea = judge(f)
            todir = "./outputdata/" + tea
            shutil.move(f, todir)
            countup(tea, shop)

    text_result.SetLabel('振り分け処理が完了しました。下記が集計結果です。')
    display_sold_count()


app = wx.App()
frame = wx.Frame(None, -1, 'タイトル', size=(1000, 300), style=wx.DEFAULT_FRAME_STYLE)

# パネル
p = wx.Panel(frame, wx.ID_ANY)

# ボタン
button_1 = wx.Button(p, wx.ID_ANY, '振り分け')
button_1.Bind(wx.EVT_BUTTON, click_button_1)

# テキスト
text_result = wx.StaticText(p, wx.ID_ANY, '')

# レイアウト
layout = wx.BoxSizer(wx.VERTICAL)
layout.Add(button_1)
layout.Add(text_result, flag=wx.EXPAND | wx.ALL, border=10)

grid_result00 = wx.StaticText(p, wx.ID_ANY, '')
grid_result01 = wx.StaticText(p, wx.ID_ANY, 'A店')
grid_result02 = wx.StaticText(p, wx.ID_ANY, 'B店')
grid_result03 = wx.StaticText(p, wx.ID_ANY, 'C店')
grid_result10 = wx.StaticText(p, wx.ID_ANY, '綾鷹')
grid_result11 = wx.StaticText(p, wx.ID_ANY, '')
grid_result12 = wx.StaticText(p, wx.ID_ANY, '')
grid_result13 = wx.StaticText(p, wx.ID_ANY, '')
grid_result20 = wx.StaticText(p, wx.ID_ANY, 'おおいお茶')
grid_result21 = wx.StaticText(p, wx.ID_ANY, '')
grid_result22 = wx.StaticText(p, wx.ID_ANY, '')
grid_result23 = wx.StaticText(p, wx.ID_ANY, '')
grid_result30 = wx.StaticText(p, wx.ID_ANY, 'おおいお茶濃い茶')
grid_result31 = wx.StaticText(p, wx.ID_ANY, '')
grid_result32 = wx.StaticText(p, wx.ID_ANY, '')
grid_result33 = wx.StaticText(p, wx.ID_ANY, '')
grid_result40 = wx.StaticText(p, wx.ID_ANY, '伊右衛門')
grid_result41 = wx.StaticText(p, wx.ID_ANY, '')
grid_result42 = wx.StaticText(p, wx.ID_ANY, '')
grid_result43 = wx.StaticText(p, wx.ID_ANY, '')
grid_result50 = wx.StaticText(p, wx.ID_ANY, '生茶')
grid_result51 = wx.StaticText(p, wx.ID_ANY, '')
grid_result52 = wx.StaticText(p, wx.ID_ANY, '')
grid_result53 = wx.StaticText(p, wx.ID_ANY, '')
grid_result60 = wx.StaticText(p, wx.ID_ANY, '天然水GREENTEA')
grid_result61 = wx.StaticText(p, wx.ID_ANY, '')
grid_result62 = wx.StaticText(p, wx.ID_ANY, '')
grid_result63 = wx.StaticText(p, wx.ID_ANY, '')

layout2 = wx.GridSizer(rows=7, cols=4, gap=(0, 0))
layout2.Add(grid_result00)
layout2.Add(grid_result01, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result02, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result03, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result10)
layout2.Add(grid_result11, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result12, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result13, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result20)
layout2.Add(grid_result21, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result22, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result23, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result30)
layout2.Add(grid_result31, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result32, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result33, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result40)
layout2.Add(grid_result41, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result42, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result43, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result50)
layout2.Add(grid_result51, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result52, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result53, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result60)
layout2.Add(grid_result61, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result62, flag=wx.ALIGN_RIGHT)
layout2.Add(grid_result63, flag=wx.ALIGN_RIGHT)

layout.Add(layout2)

p.SetSizer(layout)


frame.Show()
app.MainLoop()
