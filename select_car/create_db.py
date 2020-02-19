import sqlite3
import yaml
import os


default_yaml_filename = "config.yaml"


########################################
# DBを生成するクラス
########################################
class CreateDB:

    def __init__(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + default_yaml_filename, "r", encoding="utf-8") as f:
            y = yaml.load(stream=f, Loader=yaml.SafeLoader)
            self.db = y.get("db").get("path") + y.get("db").get("fileName")
            self.train_data_dir = y.get("train_data").get("path")

    def execute(self):
        # データベースに接続する
        conn = sqlite3.connect(self.db)
        c = conn.cursor()

        # テーブルの作成
        c.execute("CREATE TABLE cars(id int, name text, learning_file_count int, learning_count int)")

        folder = os.listdir(self.train_data_dir)
        for index, name in enumerate(folder):
            # データの挿入
            c.execute("INSERT INTO cars VALUES (" + str(index) + ", '" + name + "', 0, 0)")

        # 挿入した結果を保存（コミット）する
        conn.commit()

        # データベースへのアクセスが終わったら close する
        conn.close()




