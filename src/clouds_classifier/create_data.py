import cv2
import os
import random
import numpy
import pickle

DATADIR = "../dataset/"

ALL_CATEGORIES = [
     "clear_sky", "cirrus", "cirrocumulus", "altocumulus", "cirrostratus", "altostratus",
     "stratocumulus", "nimbostratus", "stratus", "cumulus", "cumulonimbus"
]

CLOUD_CATEGORIES = \
    [
     "clear_sky,cirrus", "cirrocumulus,altocumulus", "cirrostratus,altostratus",
     "stratocumulus", "nimbostratus,stratus", "cumulus", "cumulonimbus"
    ]


def category_class(cat):
    return CLOUD_CATEGORIES.index(cat)


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
    print("Loading clouds.")
    for cloud_category in CLOUD_CATEGORIES:
        category_img_count = 0
        for cloud in cloud_category.split(','):
            cloud_category_path = os.path.join(DATADIR, cloud)
            all_files = os.listdir(cloud_category_path)
            category_img_count += len(all_files)
            for cloud_file in os.listdir(cloud_category_path):
                cloud_path = os.path.join(cloud_category_path, cloud_file)
                processed_image = process_image(cloud_path)
                if processed_image is not None:
                    training_data.append([processed_image, category_class(cloud_category)])
        print("Category {} has {} images.".format(cloud_category, category_img_count))

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





