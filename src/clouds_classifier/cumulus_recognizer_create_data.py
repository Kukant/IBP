import cv2
import os
import random
import numpy
import pickle

DATADIRS = ["../mujdataset/"]

ALL_CATEGORIES = [
     "clear_sky", "cirrus", "cirrocumulus", "altocumulus", "cirrostratus", "altostratus",
     "stratocumulus", "nimbostratus", "stratus", "cumulus",# "cumulonimbus"
]


selected_category = "clear_sky"

IMG_SIZE = 200


def process_image(image_path):
    try:
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HLS)
        if random.random() < 0.1 and False:
            cv2.imshow('image', resized)
            cv2.waitKey(0)
        return resized
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

    with open("{}_X.pickle".format(selected_category), "wb") as fw:
        pickle.dump(X, fw)

    with open("{}_y.pickle".format(selected_category), "wb") as fw:
        pickle.dump(y, fw)

    print("Data saved successfully.")





