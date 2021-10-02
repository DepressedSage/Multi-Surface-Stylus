import cv2 as cv
import numpy as np
from screeninfo import get_monitors

arr = []


def click_event(event, x, y, flags, params):
    if event == cv.EVENT_LBUTTONDOWN:
        arr.append([x, y])
        refresh()

    if event == cv.EVENT_RBUTTONDOWN:
        arr.clear()
        refresh()


def refresh():
    cv.polylines(
        canvas, [np.array(arr)], False, (0, 0, 255), 10)
    cv.imshow('image', canvas)


if __name__ == "__main__":
    # vX, vY, L, B, lf=L/1080
    # touch, pressure, ax, ay, x, y
    # refresh rate :=> 1/acc
    canvas = np.ones((1080, 1920))
# im = cv.line(canvas, (0, 0), (255, 255), (0, 0, 0), 10)

    cv.imshow("image", canvas)
    cv.setMouseCallback('image', click_event)
    cv.waitKey(0)
    cv.destroyAllWindows()
