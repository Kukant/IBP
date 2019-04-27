from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
from keras.utils.np_utils import to_categorical
from time import time

import os
import random
import cv2
import numpy
import pickle
from datetime import datetime
import subprocess

DATADIRS = ["./mujdataset/", "./dataset/"]

RANDOM_CATEGORY = "random"

ALL_CATEGORIES = [
   "clear_sky", "cirrus", "cirrocumulus", "altocumulus", "cirrostratus", "altostratus",
    "stratocumulus", "nimbostratus", "stratus", "cumulus", "random" # "cumulonimbus"
]

ALL_CLASSES = [
   "clear_sky", "cirrus", "cirrocumulus,altocumulus", "cirrostratus", "altostratus,nimbostratus,stratus", "cumulus", "stratocumulus"
]

IMG_SIZE = 200


def lear_models(selected_category, model_name=None):
    model_name = selected_category if model_name is None else model_name
    X = pickle.load(open("{}_X.pickle".format(selected_category), "rb"))
    y = pickle.load(open("{}_y.pickle".format(selected_category), "rb"))
    X = X/255.0

    dense_layers = [0]
    layer_sizes = [32, 42, 64]
    conv_layers = [2, 3]

    for dense_layer in dense_layers:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = "{}-{}-c-{}-n-{}-d-{}".format(model_name, conv_layer, layer_size, dense_layer, int(time()))
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

                model.fit(X, y, batch_size=8, validation_split=0.3, epochs=5, callbacks=[tensorboard, ])

                model.save("./models/{}.model".format(NAME))


def process_image(image_path):
    try:
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return resized
    except Exception as e:
        print(e)
        return None


def create_data(selected_category, datadir=DATADIRS[0]):
    print("Creating data for {} category using {}".format(selected_category, datadir))

    def create_training_data():
        training_data = []
        all_imgs = {x: [] for x in [0, 1]}
        for cloud_class in ALL_CATEGORIES:
            for cloud_cat in cloud_class.split(','):
                cloud_category_path = os.path.join(datadir, cloud_cat)
                for cloud_file in os.listdir(cloud_category_path):
                    cloud_path = os.path.join(cloud_category_path, cloud_file)
                    all_imgs[1 if cloud_class in selected_category.split(",") else 0].append(cloud_path)

        selected_category_len = len(all_imgs[1])
        random.shuffle(all_imgs[0])
        all_imgs[0] = all_imgs[0][:selected_category_len]

        for img_class, img_paths in all_imgs.items():
            for img_path in img_paths:
                processed_image = process_image(img_path)
                if processed_image is not None:
                    training_data.append([processed_image, img_class])

        return training_data

    data = create_training_data()
    random.shuffle(data)

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


def clear_data():
    subprocess.call(["rm", "*.pickle"])


def get_class_index(cat):
    i = 0
    for cl in ALL_CLASSES:
        if cat in cl.split(","):
            return i
        i += 1


def create_data_categorical(aug, datadir=DATADIRS[0], category_minimum=1200):
    def process_image_c(image_path, aug):
        try:
            img_array = cv2.imread(image_path)
            resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
            rotated = cv2.rotate(resized, cv2.ROTATE_180)
            return [resized] if not aug else [resized, rotated]
        except Exception as e:
            print(e)
            return None

    def create_training_data():
        training_data = []
        all_imgs = {x: [] for x in range(ALL_CLASSES.__len__())}
        for cloud_cat in ALL_CATEGORIES:
            if cloud_cat == RANDOM_CATEGORY:
                continue
            cloud_category_path = os.path.join(datadir, cloud_cat)
            cnt = 0
            cloud_files = os.listdir(cloud_category_path)
            while cnt < category_minimum:
                cloud_path = os.path.join(cloud_category_path, cloud_files[cnt % cloud_files.__len__()])
                all_imgs[get_class_index(cloud_cat)].append(cloud_path)
                cnt += 1

        for k, v in all_imgs.items():
            random.shuffle(v)
            v = v[0:category_minimum]
            all_imgs[k] = v

        for k, v in all_imgs.items():
            print("\t{}: {}".format(k, len(v)))

        for img_class, img_paths in all_imgs.items():
            for img_path in img_paths:
                processed_image = process_image_c(img_path, aug)
                if processed_image is not None:
                    for bla in processed_image:
                        training_data.append([bla, img_class])

        return training_data

    data = create_training_data()
    random.shuffle(data)

    X = []
    y = []
    for features, label in data:
        X.append(features)
        y.append(label)

    # convert to numpy array
    X = numpy.array(X).reshape((-1, IMG_SIZE, IMG_SIZE, 3))

    with open("categorical_X.pickle", "wb") as fw:
        pickle.dump(X, fw)

    with open("categorical_y.pickle", "wb") as fw:
        pickle.dump(y, fw)


def learn_categorical(extraname="", epochs=None):
    X = pickle.load(open("categorical_X.pickle", "rb"))
    y = to_categorical(pickle.load(open("categorical_y.pickle", "rb")))
    X = X / 255.0

    if epochs is None:
        epochs = [5, 7]

    layer_sizes = [32, 42, 64]
    conv_layers = [2, 3]

    for epoch in epochs:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = "categorical-{}-conv-{}-nodes-{}-epochs-{}{}".format(conv_layer, layer_size, epoch, extraname, int(time()))
                model = Sequential()

                model.add(Conv2D(layer_size, (3, 3), input_shape=X.shape[1:]))
                model.add(Activation('relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))

                for l in range(conv_layer - 1):
                    model.add(Conv2D(layer_size, (3, 3)))
                    model.add(Activation('relu'))
                    model.add(MaxPooling2D(pool_size=(2, 2)))

                model.add(Flatten())

                model.add(Dense(len(ALL_CLASSES)))
                model.add(Activation('sigmoid'))

                tensorboard = TensorBoard(log_dir="logs/{}".format(NAME))

                model.compile(loss="categorical_crossentropy",
                              optimizer="adam",
                              metrics=["accuracy"])

                model.fit(X, y, batch_size=16, validation_split=0.3, epochs=epoch, callbacks=[tensorboard, ])

                model.save("./models/{}.model".format(NAME))


def main():
    print("time start: {}".format(datetime.utcnow()))

    try:
        os.mkdir("logs")
        os.mkdir("models")
    except Exception as e:
        print("caajk")

    create_data(RANDOM_CATEGORY, datadir=DATADIRS[1])
    lear_models(RANDOM_CATEGORY, model_name="random-old_dataset-")
    clear_data()

    create_data(RANDOM_CATEGORY)
    lear_models(RANDOM_CATEGORY)
    clear_data()

    # try to learn categorical model

    create_data_categorical(False, datadir=DATADIRS[1], category_minimum=500)
    learn_categorical(epochs=[5], extraname="-old_dataset-")

    create_data_categorical(False)
    learn_categorical()

    create_data_categorical(True)
    learn_categorical()

    clear_data()

    print("time end: {}".format(datetime.utcnow()))


main()




