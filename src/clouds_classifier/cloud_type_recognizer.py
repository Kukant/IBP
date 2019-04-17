from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
from time import time

import os
import random
import cv2
import numpy
import pickle
from datetime import datetime

DATADIRS = ["../mujdataset/"]

ALL_CATEGORIES = [
    "clear_sky", "cirrus", "cirrocumulus", "altocumulus", "cirrostratus", "altostratus",
    "stratocumulus", "nimbostratus", "stratus", "cumulus",  # "cumulonimbus"
]

IMG_SIZE = 200


def lear_models(selected_category):
    X = pickle.load(open("{}_X.pickle".format(selected_category), "rb"))
    y = pickle.load(open("{}_y.pickle".format(selected_category), "rb"))
    X = X/255.0

    dense_layers = [0]
    layer_sizes = [32, 42, 64]
    conv_layers = [2, 3]

    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = "{}-{}-c-{}-n-{}-d-{}".format(selected_category, conv_layer, layer_size, dense_layer, int(time()))
                print(NAME)
                model = Sequential()

                model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))

                for l in range(conv_layer - 1):
                    model.add(Conv2D(layer_size, (3, 3)))
                    model.add(Activation('relu'))
                    model.add(MaxPooling2D(pool_size=(2, 2)))

                model.add(Flatten())

                for _ in range(dense_layer):
                    model.add(Dense(layer_size))
                    model.add(Activation('relu'))

                model.add(Dense(1))
                model.add(Activation('sigmoid'))

                tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

                model.compile(loss="binary_crossentropy",
                              optimizer="adam",
                              metrics=["accuracy"])

                model.fit(X, y, batch_size=8, validation_split=0.3, epochs=1, callbacks=[tensorboard, ])

                model.save("./models/{}.model".format(NAME))


def create_data(selected_category):
    def process_image(image_path):
        try:
            img_array = cv2.imread(image_path)
            resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
            if random.random() < 0.1 and False:
                cv2.imshow('image', resized)
                cv2.waitKey(0)
            return hsv
        except Exception as e:
            print(e)
            return None

    def create_training_data():
        training_data = []
        print("Loading clouds.")
        all_imgs = {x: [] for x in [0, 1]}
        for cloud_class in ALL_CATEGORIES:
            for datadir in DATADIRS:
                for cloud_cat in cloud_class.split(','):
                    cloud_category_path = os.path.join(datadir, cloud_cat)
                    for cloud_file in os.listdir(cloud_category_path):
                        cloud_path = os.path.join(cloud_category_path, cloud_file)
                        all_imgs[1 if selected_category == cloud_class else 0].append(cloud_path)

        selected_category_len = len(all_imgs[1])
        random.shuffle(all_imgs[0])
        all_imgs[0] = all_imgs[0][:selected_category_len]

        print("{} count is {}".format(selected_category, selected_category_len))

        for img_class, img_paths in all_imgs.items():
            for img_path in img_paths:
                processed_image = process_image(img_path)
                if processed_image is not None:
                    training_data.append([processed_image, img_class])

        return training_data

    data = create_training_data()
    random.shuffle(data)

    print("Shuffled data: ")
    for s in data[:100]:
        print(s[1], end="")

    X = []
    y = []
    for features, label in data:
        X.append(features)
        y.append(label)

    # convert to numpy array
    X = numpy.array(X).reshape((-1, IMG_SIZE, IMG_SIZE, 3))

    with open("{}_X.pickle".format(selected_category), "wb") as fw:
        pickle.dump(X, fw)
        print("{}_X.pickle saved.".format(selected_category))

    with open("{}_y.pickle".format(selected_category), "wb") as fw:
        pickle.dump(y, fw)


if __name__ == "__main__":
    print("time start: {}".format(datetime.utcnow()))

    os.mkdir("logs")
    os.mkdir("models")
    for cat in ALL_CATEGORIES:
        create_data(cat)

    for cat in ALL_CATEGORIES:
        lear_models(cat)

    print("time end: {}".format(datetime.utcnow()))




