import cv2
import keras
import numpy

FILE = "nemrak2.jpg"
IMG_SIZE = 200


def process_image(image_path):
    try:
        img_array = cv2.imread(image_path)
        resized = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
        return numpy.array(resized).reshape((-1, IMG_SIZE, IMG_SIZE, 3))/255

    except Exception as e:
        return None


img = process_image(FILE)
model = keras.models.load_model("2-conv-32-nodes-0-dense-1549853225.model")

prediction = model.predict([img])
print(prediction)

