import cv2
import os
import random
import numpy
import pickle

DATADIRS = ["../mujdataset/", "../dataset/"]

ALL_CATEGORIES = [
     "clear_sky", "cirrus", "cirrocumulus", "altocumulus", "cirrostratus", "altostratus",
     "stratocumulus", "nimbostratus", "stratus", "cumulus",# "cumulonimbus"
]

CLOUD_CATEGORIES = \
    [
     "clear_sky,cirrus", "cirrocumulus,altocumulus", "cirrostratus,altostratus",
     "stratocumulus", "nimbostratus,stratus", "cumulus", #"cumulonimbus"
    ]


def category_class(cat):
    return ALL_CATEGORIES.index(cat)


IMG_SIZE = 200


def process_image(image_path):
    try:
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return resized
    except Exception as e:
        print(e)
        return None


def create_training_data():
    training_data = []
    print("Loading clouds.")
    all_imgs = { x: [] for x in range(len(ALL_CATEGORIES))}
    for cloud_class in ALL_CATEGORIES:
        for datadir in DATADIRS:
            for cloud_cat in cloud_class.split(','):
                cloud_category_path = os.path.join(datadir, cloud_cat)
                for cloud_file in os.listdir(cloud_category_path):
                    cloud_path = os.path.join(cloud_category_path, cloud_file)
                    all_imgs[category_class(cloud_class)].append(cloud_path)

    for img_class, img_paths in all_imgs.items():
        for img_path in img_paths:
            processed_image = process_image(img_path)
            if processed_image is not None:
                training_data.append([processed_image, img_class])

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





