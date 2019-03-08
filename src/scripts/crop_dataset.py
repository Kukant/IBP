import cv2
import numpy as np
import glob
import os


def get_border_row(img):
    # goes from top to bottom
    h, w = img.shape
    no_hits_stop = int(h/6)
    no_hits = 0
    treshold = 125

    border = 0
    no_hits_in_row = 0
    for r in range(int(h/2 - 1)):
        row_value = img[r:r + 1].sum() / w
        if row_value > treshold:
            no_hits += 1
            no_hits_in_row += 1
            if no_hits >= no_hits_stop:
                if abs(no_hits - r) < 10:
                    return 0
                else:
                    return border - no_hits_in_row
        else:
            no_hits = no_hits - 1 if no_hits > 1 else 0
            no_hits_in_row = 0
        border = r

    return border


def prop_zeros(img):
    binary_mask = np.copy(img)
    h, w = binary_mask.shape
    res = np.full((h, w), 255, dtype=np.uint8)

    # crop = [(y, y + h), (x, x + h)]
    crop = [[0, 0], [0, 0]]

    b = get_border_row(binary_mask)
    crop[0][0] = b
    for i in range(0, b):
        res[i:i+1] = 0

    for i in range(0, b):
        binary_mask[i:i + 1] = 255

    for bla in range(3):
        res = cv2.rotate(res, cv2.ROTATE_90_CLOCKWISE)
        binary_mask = cv2.rotate(binary_mask, cv2.ROTATE_90_CLOCKWISE)

        #cv2.imshow("rotated {}".format(bla), img)
        b = get_border_row(binary_mask)
        for i in range(0, b):
            res[i:i+1] = 0

        for i in range(0, b):
            binary_mask[i:i + 1] = 255

        if bla == 0:
            crop[1][0] = b
        elif bla == 1:
            crop[0][1] = h - b
        elif bla == 2:
            crop[1][1] = w - b

    res = cv2.rotate(res, cv2.ROTATE_90_CLOCKWISE)

    return res, crop


def get_color_mask(hsv):
    lower_blue = np.array([79, 10, 0], np.uint8)
    upper_blue = np.array([132, 255, 255], np.uint8)

    lower_white = np.array([0, 185, 0], np.uint8)
    upper_white = np.array([255, 255, 255], np.uint8)

    lower_grey = np.array([0, 0, 0], np.uint8)
    upper_grey = np.array([255, 255, 30], np.uint8)

    #lower_dgrey = np.array([0, 48, 0], np.uint8)
    #upper_dgrey = np.array([20, 122, 255], np.uint8)

    #lower_orange = np.array([10, 33, 0], np.uint8)
  #  upper_orange = np.array([33, 255, 255], np.uint8)

    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    white_mask = cv2.inRange(hsv, lower_white, upper_white)
    grey_mask = cv2.inRange(hsv, lower_grey, upper_grey)
    #dgrey_mask = cv2.inRange(hsv, lower_dgrey, upper_dgrey)
    #orange_mask = cv2.inRange(hsv, lower_orange, upper_orange)

    mask = cv2.bitwise_or(blue_mask, white_mask)
    mask = cv2.bitwise_or(mask, grey_mask)
    #mask = cv2.bitwise_or(mask, dgrey_mask)
    #mask = cv2.bitwise_or(mask, orange_mask)

    # pridat hodne tmave modrou, oranzovou
    return mask


for filename in glob.iglob("../dataset/**/*.jpg", recursive=True):
    if "random" in filename or "clear_sky" in filename:
        continue
    impath = filename
    #impath = "test.jpg"
    img = cv2.imread(impath)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

    color_mask = get_color_mask(hsv)

    prop_mask, crop = prop_zeros(color_mask)

    prop = cv2.bitwise_and(img, img, mask=prop_mask)
    color = cv2.bitwise_and(img, img, mask=color_mask)

    cropped = img[crop[0][0]:crop[0][1], crop[1][0]:crop[1][1]]

    original = cv2.resize(img, (500, 500))
    prop = cv2.resize(prop, (500, 500))

    cv2.putText(original, "({})".format(filename), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.putText(prop, "({})".format(filename), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.imshow("original", original)
    cv2.imshow("colorfilter", cv2.resize(color, (500, 500)))
    #cv2.imshow("cropped", cv2.resize(cropped, (500, 500)))
    cv2.imshow("prop", prop)

    print("Processing {}: ".format(filename), end="")
    ret = cv2.waitKey(0)
    if ret == 13: # enter hit
        cv2.imwrite(filename[:-3] + "jpeg", cropped)
        os.remove(filename)
        print("Cropped file saved.")
    elif ret == 8: # del hit
        os.remove(filename)
        print("File removed")
    else:
        cv2.imwrite(filename[:-3] + "jpeg", img)
        os.remove(filename)
        print("ok")
        continue

cv2.destroyAllWindows()


