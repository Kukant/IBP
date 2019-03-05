import cv2
import os
import random
import numpy
import pickle


DATADIR = "../dataset/"
CLOUD_CATEGORIES = \
    [
     "altocumulus", "altostratus", "cirrocumulus", "cirrostratus",
     "cirrus", "cumulonimbus", "cumulus",
     "nimbostratus", "stratocumulus", "stratus"
    ]
RANDOM_CATEGORY = "random"
CLOUD_CLASS = 1
OTHER_CLASS = 0
IMG_SIZE = 200


def process_image(image_path):
    try:
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return resized
    except Exception as e:
        return None


def create_training_data():
    training_data = []
    i = 0
    print("Loading clouds.")
    for cloud_category in CLOUD_CATEGORIES:
        cloud_category_path = os.path.join(DATADIR, cloud_category)
        for cloud in os.listdir(cloud_category_path):
            cloud_path = os.path.join(cloud_category_path, cloud)
            processed_image = process_image(cloud_path)
            if processed_image is not None:
                training_data.append([processed_image, CLOUD_CLASS])

    print("Loading random.")
    random_images_path = os.path.join(DATADIR, RANDOM_CATEGORY)
    for random_image in os.listdir(random_images_path):
        random_image_path = os.path.join(random_images_path, random_image)
        processed_image = process_image(random_image_path)
        if processed_image is not None:
            training_data.append([processed_image, OTHER_CLASS])

    print("Data loaded.")
    return training_data


if __name__ == "__main__":
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

    with open("X.pickle", "wb") as fw:
        pickle.dump(X, fw)

    with open("y.pickle", "wb") as fw:
        pickle.dump(y, fw)

    print("Data saved successfully.")





