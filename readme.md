# select_car（入力した車の画像の種類を判定するアプリ）

# ■アプリ

- (必須)各種ディレクトリパスはconfig.yamlで指定されているため、各自修正すること
- `application.py`を実行して起動する
- 「testdata」内の画像をドラッグ＆ドロップすると結果が表示される

# ■学習

- アプリを起動し、`Learning Maintenance`タグの「学習を実施」ボタンを押下する
- `learning.py`の77～82行目で学習用の画像を10倍に増幅させているため、増幅を行わない場合はこの部分をコメントアウトする


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
アプリを起動する場合には`application.py`を実行すれば起動する。