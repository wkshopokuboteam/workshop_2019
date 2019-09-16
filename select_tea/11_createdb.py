# 必要モジュールをインポートする
import sqlite3

# データベースに接続する
conn = sqlite3.connect('database/example.db')
c = conn.cursor()

# テーブルの作成
c.execute("CREATE TABLE teas(id int, name text, count int)")

# データの挿入
c.execute("INSERT INTO teas VALUES (0, '綾鷹', 0)")
c.execute("INSERT INTO teas VALUES (1, 'おおいお茶', 0)")
c.execute("INSERT INTO teas VALUES (2, 'おおいお茶濃い茶', 0)")
c.execute("INSERT INTO teas VALUES (3, '伊右衛門', 0)")
c.execute("INSERT INTO teas VALUES (4, '生茶', 0)")
c.execute("INSERT INTO teas VALUES (5, '天然水GREENTEA', 0)")
c.execute("INSERT INTO teas VALUES (6, '識別不能', 0)")

# 挿入した結果を保存（コミット）する
conn.commit()

# データベースへのアクセスが終わったら close する
conn.close()

