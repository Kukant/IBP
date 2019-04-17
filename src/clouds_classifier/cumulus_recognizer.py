import pickle
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.callbacks import TensorBoard
from time import time

selected_category = "clear_sky"
X = pickle.load(open("{}_X.pickle".format(selected_category), "rb"))
y = pickle.load(open("{}_y.pickle".format(selected_category), "rb"))
X = X/255.0

dense_layers = [0]
layer_sizes = [42]
conv_layers = [2]

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

            model.save("{}.model".format(NAME))






