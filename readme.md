# select_tea（入力した緑茶の画像の種類を判定するアプリ）

# ■データベースの作成

- 「11_createdb.py」でデータベースとテーブルを作成し、レコードを挿入する
- 「12_selectdb.py」でデータの一覧を取得する

※データベースは「database」内の「example.db」として保存される

# ■学習

- 「01_makedata.py」で「testdata」内の画像データを学習用に変換し、「learningresult」に保存する
- 「02_learning.py」で定義した学習モデルに従って学習を行い、結果を「learningresult」に保存する

# ■アプリ

- 「A1_app.py」を実行して起動する
- 「testdata」内の画像をドラッグ＆ドロップすると結果が表示される

　各種類の選択回数もデータベースに更新され、合わせて表示される


# agg_tea（緑茶の画像の振り分けと集計を行うアプリ）

# ■データベースの作成
# ■学習

- 「select_tea」と同じ

# ■アプリ

- 「A1_app.py」を実行して起動する
- 「inputdata」の各店舗のフォルダに画像を格納する
- 「振り分け」ボタンを押下する
- 「inputdata」の画像が緑茶の種類により「outputdata」に振り分けられる
- 合わせて緑茶の種類と店舗毎の集計結果（累計）が表示される


# select_car（入力した車の画像の種類を判定するアプリ）

# ■学習

- 「01_learning.py」を実行して、「traindata」内の画像を学習させ、結果を「learningresult」に保存する
- 57～62行目で学習用の画像を10倍に増幅させているため、増幅を行わない場合はこの部分をコメントアウトする

# ■アプリ

- 「A1_app.py」を実行して起動する
- 「testdata」内の画像をドラッグ＆ドロップすると結果が表示される



# 開発環境の構築方法
## ①pycharmでProjectをオープンする
## ②環境変数を追加する
terminalから下記を実行すること  
`set PIPENV_VENV_IN_PROJECT=1`  
`set PIPENV_IGNORE_VIRTUALENVS=1`

## ③仮想実行環境を構築
ternalから `pipenv install`を実行する  
プロジェクト直下に `.venv`が構築されていることを確認する。

## ④インタプリタを仮想実行環境に変更する
左上のFile→Settings→Project Interpreterにてインタプリタを `~/.venv/Scripts/Python.exe`に変更する

## ⑤構築はこれで完了
アプリを起動する場合にはterminalで `pipenv run start`を実行すれば起動する。