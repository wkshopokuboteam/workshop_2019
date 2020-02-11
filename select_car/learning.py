from PIL import Image
import glob
import random, math
from keras import layers, models, regularizers
from keras import optimizers
from keras.layers import Dropout
from keras.utils import np_utils
import numpy as np
import os
import matplotlib.pyplot as plt
from keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array, array_to_img
import sqlite3
import yaml

default_yaml_filename = "config.yaml"
epoch_count = 20


########################################
# ラベリングによる学習/検証データの準備
########################################
class Learning:
    def __init__(self):
        with open(os.path.dirname(os.path.abspath(__file__)) + os.sep + default_yaml_filename, "r", encoding="utf-8") as f:
            y = yaml.load(stream=f, Loader=yaml.SafeLoader)
            self.db = y.get("db").get("path") + y.get("db").get("fileName")
            self.train_data_dir = y.get("train_data").get("path")
            self.result = y.get("result")

    # 画像を拡張する関数
    def draw_images(self, generator, x, output_dir, index):
        save_name = 'extened-' + str(index)
        g = generator.flow(x, batch_size=1, save_to_dir=output_dir,
                           save_prefix=save_name, save_format='jpg')

        # 1つの入力画像から何枚拡張するかを指定（今回は10枚）
        for i in range(10):
            bach = g.next()

    def execute(self):

        # ImageDataGeneratorを定義
        datagen = ImageDataGenerator(rotation_range=30,
                                     width_shift_range=20,
                                     height_shift_range=0.,
                                     zoom_range=0.1,
                                     horizontal_flip=True,
                                     vertical_flip=True)

        # ファイル読込
        folder = os.listdir(self.train_data_dir)
        image_size = 150
        dense_size = len(folder)

        X_train = []
        X_test = []
        y_train = []
        y_test = []
        size_count = []
        learning_count = []

        for index, name in enumerate(folder):
            dir = self.train_data_dir + name
            files = glob.glob(dir + "/*.jpg")
            random.shuffle(files)
            th = math.floor(len(files) * 0.8)
            train = files[0:th]
            test = files[th:]
            size_count.append((index, len(files)))
            learning_count.append((index, epoch_count))

            # 出力先ディレクトリの設定
            output_dir = "./expand/" + name
            if not (os.path.exists(output_dir)):
                os.mkdir(output_dir)
            # 読み込んだ画像を順に拡張（拡張しない場合は下記をコメントアウト）
            # for i in range(len(train)):
                #     img = load_img(train[i])
                #     x = img_to_array(img)
                #     x = np.expand_dims(x, axis=0)
            #     self.draw_images(datagen, x, output_dir, i)
            # train = glob.glob(output_dir + "/*.jpg")
            for i, file in enumerate(train):
                image = Image.open(file)
                image = image.convert("RGB")
                image = image.resize((image_size, image_size))
                data = np.asarray(image)
                X_train.append(data)
                y_train.append(index)
            for i, file in enumerate(test):
                image = Image.open(file)
                image = image.convert("RGB")
                image = image.resize((image_size, image_size))
                data = np.asarray(image)
                X_test.append(data)
                y_test.append(index)

        X_train = np.array(X_train)
        X_test = np.array(X_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)
        X_train = X_train.astype('float32')
        X_train = X_train / 255.0
        X_test = X_test.astype('float32')
        X_test = X_test / 255.0

        y_train = np_utils.to_categorical(y_train, dense_size)
        y_test = np_utils.to_categorical(y_test, dense_size)

        # モデルの構築

        model = models.Sequential()
        model.add(layers.Conv2D(32, (3, 3), activation="relu", input_shape=(150, 150, 3)))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(64, (3, 3), activation="relu"))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation="relu"))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Conv2D(128, (3, 3), activation="relu"))
        model.add(layers.MaxPooling2D((2, 2)))
        model.add(layers.Flatten())
        # ドロップアウトを追加
        model.add(Dropout(0.5))
        # L2正則化を追加（kernel_regularizerオプション）
        model.add(layers.Dense(512, kernel_regularizer=regularizers.l2(0.001), activation="relu"))
        # 分類先の種類分設定
        model.add(layers.Dense(10, activation="softmax"))

        # モデル構成の確認
        model.summary()

        # モデルのコンパイル
        model.compile(loss="categorical_crossentropy",
                      optimizer=optimizers.RMSprop(lr=1e-4),
                      metrics=["acc"])

        # モデルの学習

        model = model.fit(X_train,
                          y_train,
                          epochs=epoch_count,
                          batch_size=10,
                          validation_data=(X_test, y_test))

        # 学習結果を表示

        acc = model.history['acc']
        val_acc = model.history['val_acc']
        loss = model.history['loss']
        val_loss = model.history['val_loss']

        epochs = range(len(acc))

        plt.plot(epochs, acc, 'bo', label='Training acc')
        plt.plot(epochs, val_acc, 'b', label='Validation acc')
        plt.title('Training and validation accuracy')
        plt.legend()
        plt.savefig(self.result.get("path") + self.result.get("fit"))

        plt.figure()

        plt.plot(epochs, loss, 'bo', label='Training loss')
        plt.plot(epochs, val_loss, 'b', label='Validation loss')
        plt.title('Training and validation loss')
        plt.legend()
        plt.savefig(self.result.get("path") + self.result.get("const"))

        # モデルの保存

        json_string = model.model.to_json()
        open(self.result.get("path") + self.result.get("model"), 'w').write(json_string)

        # 重みの保存

        hdf5_file = self.result.get("path") + self.result.get("weight")
        model.model.save_weights(hdf5_file)

        # データ更新
        conn = sqlite3.connect(self.db)
        c = conn.cursor()
        for item in size_count:
            c.execute("UPDATE cars SET learning_file_count = ? WHERE id = ?", (item[1], item[0]))
        conn.commit()
        for item in learning_count:
            c.execute("UPDATE cars SET learning_count = ? WHERE id = ?", (item[1], item[0]))
        conn.commit()
        conn.close()
