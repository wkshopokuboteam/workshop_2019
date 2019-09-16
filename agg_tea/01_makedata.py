# ラベリングによる学習/検証データの準備

from PIL import Image
import glob
import numpy as np
import random
import math


# 画像が保存されているルートディレクトリのパス
root_dir = 'traindata'
# 商品名
categories = ['綾鷹', 'おおいお茶', 'おおいお茶濃い茶', '伊右衛門', '生茶', '天然水GREENTEA']

# 画像データ用配列
X = []
# ラベルデータ用配列
Y = []


# 画像データごとにadd_sample()を呼び出し、X,Yの配列を返す関数
def make_sample(files):
    global X, Y
    X = []
    Y = []
    for cat, fname in files:
        add_sample(cat, fname)
    return np.array(X), np.array(Y)


# 渡された画像データを読み込んでXに格納し、また、
# 画像データに対応するcategoriesのidxをY格納する関数
def add_sample(cat, fname):
    img = Image.open(fname)
    img = img.convert("RGB")
    img = img.resize((150, 150))
    data = np.asarray(img)
    X.append(data)
    Y.append(cat)


# 全データ格納用配列
allfiles = []


# カテゴリ配列の各値と、それに対応するidxを認識し、全データをallfilesにまとめる
for idx, cat in enumerate(categories):
    image_dir = root_dir + "/" + cat
    files = glob.glob(image_dir + "/*.jpg")
    for f in files:
        allfiles.append((idx, f))


# シャッフル後、学習データと検証データに分ける
random.shuffle(allfiles)
th = math.floor(len(allfiles) * 0.8)
train = allfiles[0:th]
test = allfiles[th:]
X_train, y_train = make_sample(train)
X_test, y_test = make_sample(test)
xy = (X_train, X_test, y_train, y_test)
# データを保存する（データの名前を「tea_data.npy」としている）
np.save("learningresult/tea_data.npy", xy)
