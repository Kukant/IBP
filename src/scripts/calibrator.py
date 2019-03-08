import numpy as np
import cv2 as cv
import time


path = "../dataset/cirrostratus/{}.jpg".format(35)
#path = "chart.jpg"
img = cv.imread(path, cv.IMREAD_COLOR)
img = cv.resize(img, (600, 600))
#img = cv.medianBlur(img,5)

# Convert BGR to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HLS)

l = [0, 135, 0]
u = [255, 255, 30]

uh = u[0]
us = u[1]
uv = u[2]
lh = l[0]
ls = l[1]
lv = l[2]
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])

mask = cv.inRange(hsv, lower_hsv, upper_hsv)
window_name = "HSV Calibrator"
cv.namedWindow(window_name)

def nothing(x):
    print("Trackbar value: " + str(x))
    pass

# create trackbars for Upper HSV
cv.createTrackbar('UpperH',window_name,0,255,nothing)
cv.setTrackbarPos('UpperH',window_name, uh)

cv.createTrackbar('UpperS',window_name,0,255,nothing)
cv.setTrackbarPos('UpperS',window_name, us)

cv.createTrackbar('UpperV',window_name,0,255,nothing)
cv.setTrackbarPos('UpperV',window_name, uv)

# create trackbars for Lower HSV
cv.createTrackbar('LowerH',window_name,0,255,nothing)
cv.setTrackbarPos('LowerH',window_name, lh)

cv.createTrackbar('LowerS',window_name,0,255,nothing)
cv.setTrackbarPos('LowerS',window_name, ls)

cv.createTrackbar('LowerV',window_name,0,255,nothing)
cv.setTrackbarPos('LowerV',window_name, lv)

font = cv.FONT_HERSHEY_SIMPLEX

while(1):
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)
    cv.putText(mask,'Lower HSV: [' + str(lh) +',' + str(ls) + ',' + str(lv) + ']', (10,30), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    cv.putText(mask,'Upper HSV: [' + str(uh) +',' + str(us) + ',' + str(uv) + ']', (10,60), font, 0.5, (200,255,155), 1, cv.LINE_AA)

    toshow = cv.bitwise_and(img, img ,mask = mask)
    cv.imshow(window_name,toshow)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of Upper HSV trackbars
    uh = cv.getTrackbarPos('UpperH',window_name)
    us = cv.getTrackbarPos('UpperS',window_name)
    uv = cv.getTrackbarPos('UpperV',window_name)
    upper_blue = np.array([uh,us,uv])
    # get current positions of Lower HSCV trackbars
    lh = cv.getTrackbarPos('LowerH',window_name)
    ls = cv.getTrackbarPos('LowerS',window_name)
    lv = cv.getTrackbarPos('LowerV',window_name)
    upper_hsv = np.array([uh,us,uv])
    lower_hsv = np.array([lh,ls,lv])

    time.sleep(.1)

cv.destroyAllWindows()