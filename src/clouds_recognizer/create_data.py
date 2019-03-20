import cv2
import os
import random
import numpy
import pickle


DATADIR = "../mujdataset/"
CLOUD_CATEGORIES = \
    [
     "altocumulus", "altostratus", "cirrocumulus", "cirrostratus",
     "cirrus", "cumulonimbus", "cumulus",
     "nimbostratus", "stratocumulus", "stratus", "clear_sky"
    ]
RANDOM_CATEGORY = "random"
CLOUD_CLASS = 1
OTHER_CLASS = 0
IMG_SIZE = 200


def process_image(image_path, augumentation=False):
    try:
        ret = []
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        ret.append(resized)
        if augumentation:
            for rotation in [cv2.ROTATE_90_CLOCKWISE, cv2.ROTATE_90_COUNTERCLOCKWISE, cv2.ROTATE_180]:
                ret.append(cv2.rotate(resized, rotation))
        return ret
    except Exception as e:
        return None


def create_training_data():
    training_data = []
    clouds_cnt = 0
    print("Loading clouds.")
    for cloud_category in CLOUD_CATEGORIES:
        cloud_category_path = os.path.join(DATADIR, cloud_category)
        for cloud in os.listdir(cloud_category_path):
            cloud_path = os.path.join(cloud_category_path, cloud)
            processed_images = process_image(cloud_path, augumentation=False)
            if processed_images is not None:
                clouds_cnt += 1
                for img in processed_images:
                    training_data.append([img, CLOUD_CLASS])

    random_cnt = 0
    print("Loading random.")
    for datadir in [DATADIR, "../dataset/"]:
        random_images_path = os.path.join(datadir, RANDOM_CATEGORY)
        for random_image in os.listdir(random_images_path):
            random_image_path = os.path.join(random_images_path, random_image)
            processed_images = process_image(random_image_path, augumentation=False)
            if processed_images is not None:
                for img in processed_images:
                    training_data.append([img, OTHER_CLASS])
                    random_cnt += 1
                    if random_cnt >= clouds_cnt:
                        print("Data loaded.")
                        print("Processed {}/{} clouds/random".format(clouds_cnt, random_cnt))
                        return training_data

    print("Data loaded.")
    print("Processed {}/{} clouds/random".format(clouds_cnt, random_cnt))

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





