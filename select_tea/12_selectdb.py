# 必要モジュールをインポートする
import sqlite3

# データベースに接続する
conn = sqlite3.connect('database/example.db')
c = conn.cursor()

# レコードを取得する
for row in c.execute("SELECT * FROM teas ORDER BY id"):
    print(row)

# データベースへのアクセスが終わったら close する
conn.close()

