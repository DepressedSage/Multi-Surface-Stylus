import cv2 as cv
import numpy as np
from screeninfo import get_monitors


for m in get_monitors():
    ms = str(m)
    print(ms[ms.index("width")+6:ms.index("width")+10],
          ms[ms.index("height")+6:ms.index("height")+10])

# vX, vY, L, B, lf=L/1080
# touch, pressure, ax, ay, x, y
# refresh rate :=> 1/acc

canvas = np.ones((1080, 1920))
#im = cv.line(canvas, (0, 0), (255, 255), (0, 0, 0), 10)
curv = cv.polylines(
    canvas, [np.array([[0, 0], [100, 5], [200, 50]])], False, (0, 0, 255), 10)
cv.imshow("white", canvas)
cv.waitKey(0)
cv.destroyAllWindows()
