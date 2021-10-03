import cv2 as cv
import numpy as np
from screeninfo import get_monitors

arr = []

for m in get_monitors():
    ms = str(m)
    # get monitor info from ms

# vX, vY, L, B, lf=L/1080
# touch, pressure, ax, ay, x, y
# refresh rate :=> 1/acc

canvas = np.ones((1080, 1920))
#im = cv.line(canvas, (0, 0), (255, 255), (0, 0, 0), 10)

cv.imshow("white", canvas)
cv.waitKey(0)
cv.destroyAllWindows()
