import cv2 as cv
import numpy as np
from screeninfo import get_monitors


for m in get_monitors():
    ms = str(m)
    print(ms[ms.index("width")+6:ms.index("width")+10],
          ms[ms.index("height")+6:ms.index("height")+10])

arr = []

thresh = 0.1
pressure,x,y=0,0,0          #get from calculate.py


def write(x, y):
    arr.append([x, y])
    refresh()


def cleararr():
    arr.clear()
    refresh()


def refresh():
    cv.polylines(
        canvas, [np.array(arr)], False, (0, 0, 255), 10)
    cv.imshow('image', canvas)


if __name__ == "__main__":
    # vX, vY, L, B, lf=L/1080
    # touch, pressure, ax, ay, x, y

    canvas = np.ones((1080, 1920))

    while(1):
        if(pressure > thresh):
            write(x, y)
        else:
            cleararr()

    cv.imshow("image", canvas)
    cv.waitKey(0)
    cv.destroyAllWindows()
