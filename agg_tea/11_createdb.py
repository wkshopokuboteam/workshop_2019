# 必要モジュールをインポートする
import sqlite3

# データベースに接続する
conn = sqlite3.connect('database/example.db')
c = conn.cursor()

# テーブルの作成
c.execute("CREATE TABLE teas(id int, tea text, shop test, count int)")

# データの挿入
c.execute("INSERT INTO teas VALUES (0, '綾鷹', 'A店', 0)")
c.execute("INSERT INTO teas VALUES (1, 'おおいお茶', 'A店', 0)")
c.execute("INSERT INTO teas VALUES (2, 'おおいお茶濃い茶', 'A店', 0)")
c.execute("INSERT INTO teas VALUES (3, '伊右衛門', 'A店', 0)")
c.execute("INSERT INTO teas VALUES (4, '生茶', 'A店', 0)")
c.execute("INSERT INTO teas VALUES (5, '天然水GREENTEA', 'A店', 0)")
c.execute("INSERT INTO teas VALUES (6, '識別不能', 'A店', 0)")

c.execute("INSERT INTO teas VALUES (0, '綾鷹', 'B店', 0)")
c.execute("INSERT INTO teas VALUES (1, 'おおいお茶', 'B店', 0)")
c.execute("INSERT INTO teas VALUES (2, 'おおいお茶濃い茶', 'B店', 0)")
c.execute("INSERT INTO teas VALUES (3, '伊右衛門', 'B店', 0)")
c.execute("INSERT INTO teas VALUES (4, '生茶', 'B店', 0)")
c.execute("INSERT INTO teas VALUES (5, '天然水GREENTEA', 'B店', 0)")
c.execute("INSERT INTO teas VALUES (6, '識別不能', 'B店', 0)")

c.execute("INSERT INTO teas VALUES (0, '綾鷹', 'C店', 0)")
c.execute("INSERT INTO teas VALUES (1, 'おおいお茶', 'C店', 0)")
c.execute("INSERT INTO teas VALUES (2, 'おおいお茶濃い茶', 'C店', 0)")
c.execute("INSERT INTO teas VALUES (3, '伊右衛門', 'C店', 0)")
c.execute("INSERT INTO teas VALUES (4, '生茶', 'C店', 0)")
c.execute("INSERT INTO teas VALUES (5, '天然水GREENTEA', 'C店', 0)")
c.execute("INSERT INTO teas VALUES (6, '識別不能', 'C店', 0)")

# 挿入した結果を保存（コミット）する
conn.commit()

# データベースへのアクセスが終わったら close する
conn.close()

