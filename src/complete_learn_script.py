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
from itertools import cycle

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


def get_class_index(cat):
    i = 0
    for cl in ALL_CLASSES:
        if cat in cl.split(","):
            return i
        i += 1


def process_image(image_path, rotation):
    try:
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return resized if rotation is None else cv2.rotate(resized, rotation)
    except Exception as e:
        print(e)
        return None


def get_all_filepaths(augment, validation_split=0.3, category_minimum=25, datadir=DATADIRS[0]):
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
            processed_image = process_image(img_path, False)
            if processed_image is not None:
                training_data.append([img_path, img_class, None])
                if augment:
                    training_data.append([img_path, img_class, cv2.ROTATE_180])

    random.shuffle(training_data)
    validation_count = int(validation_split*len(training_data) - 0.5)
    validation_data = training_data[:validation_count]
    training_data = training_data[validation_count:]

    return validation_data, training_data


def data_generator(training_data, batch_size):
    idx = 0
    X = []
    y = []
    for sample in cycle(training_data):
        if idx == batch_size:
            X = numpy.array(X).reshape((-1, IMG_SIZE, IMG_SIZE, 3))
            X = X/255.0
            yield X, to_categorical(y, num_classes=len(ALL_CLASSES))

            X = []
            y = []
            idx = 0

        filename = sample[0]
        _class = sample[1]
        rotation = sample[2]

        processed_image = process_image(filename, rotation)
        if processed_image is None:
            continue

        X.append(processed_image)
        y.append(_class)

        idx += 1


def learn_categorical(extraname="", epochs=None, augment=True):
    if epochs is None:
        epochs = [5, 7]

    layer_sizes = [32, 64]
    conv_layers = [3, 4]

    validation_data, training_data = get_all_filepaths(augment)

    for epoch in epochs:
        for layer_size in layer_sizes:
            for conv_layer in conv_layers:
                NAME = "categorical-{}-conv-{}-nodes-{}-epochs-{}{}".format(conv_layer, layer_size, epoch, extraname, int(time()))
                print("Training {}".format(NAME))
                model = Sequential()

                model.add(Conv2D(layer_size, (3, 3), input_shape=(IMG_SIZE, IMG_SIZE, 3)))
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

                batch_size = 16
                model.fit_generator(generator=data_generator(training_data, batch_size),
                                    validation_data=data_generator(validation_data, batch_size),
                                    steps_per_epoch=int(len(training_data)/batch_size - 1),
                                    validation_steps=int(len(validation_data)/batch_size - 1),
                                    epochs=epoch,
                                    callbacks=[tensorboard, ],
                                    use_multiprocessing=True)

                model.save("./models/{}.model".format(NAME))


def main():
    global IMG_SIZE
    print("time start: {}".format(datetime.utcnow()))

    try:
        os.mkdir("logs")
    except Exception as e:
        print("caajk")

    try:
        os.mkdir("models")
    except Exception as e:
        print("caajk")

    learn_categorical(extraname="=augmentation200=", augment=True)

    IMG_SIZE = 300
    learn_categorical(extraname="=augmentation300=", augment=True)

    print("time end: {}".format(datetime.utcnow()))


main()




