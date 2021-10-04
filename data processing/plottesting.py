import time
import numpy as np
import json
import cv2 as cv
import math
from screeninfo import get_monitors

# defining required variables
rr = 0.1           # refresh rate
Xa = np.array([0, 0, 0])     # Angles of XYZ wrt ijk
ao1 = np.array([0, 0])       # last to last acceleration
vo1 = np.array([0, 0])       # last to last velocity vector
ao = np.array([0, 0])        # last acceleration
vo = np.array([0, 0])        # last velocity vector
xo = np.array([0, 0])        # last coordinate
Af = np.array([0, 0])        # current acceleration
we = False         # whether to write or erase
pThresh = 0.1      # pressure threshold for activation
arr = []           # array to store points till plotting
A = np.array([0, 0, 0])      # acceleration vector
G = np.array([0, 0, 0])      # gyroscopic readings
P = 1              # pressure


def JSONRead(JSONstr):
    global A, G, P, we
    readings = json.loads(JSONstr)

    ax = readings["accX"]
    ay = readings["accY"]
    az = readings["accZ"]
    gx = readings["gyroX"]
    gy = readings["gyroY"]
    gz = readings["gyroZ"]
    P = readings["pressure"]
    we = readings["erase"]
    A = np.array([ax, ay, az])
    G = np.array([gx, gy, gz])


def getAngle(x, g):
    x = x+g*rr
    return x


def changeCoordinateSystem(A, G, Xa):
    ax, ay, az = A
    gx, gy, gz = G
    xa, ya, za = Xa

    xa = getAngle(xa, gx)
    ya = getAngle(ya, gy)
    za = getAngle(za, gz)

    # list of universal coordinate unit vectors
    U = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    # list of relative coordinate unit vectors wrt MPU
    R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    # [                   cos(z)cos(y),               math.sin(z)cos(y),      -sin(y)]              # transformation matrix for R->U
    # [sin(x)sin(y)cos(z)-sin(x)cos(x), sin(x)sin(y)sin(z)+cos(x)cos(z), cos(y)sin(x)]              # cross multiply with U to get R in terms of U
    # [cos(x)sin(y)cos(z)+sin(x)sin(z), cos(x)sin(y)sin(z)-sin(x)cos(z), cos(x)cos(y)]              # x,y,z are angular displacements in their respective axes

    T = [[math.cos(za)*math.cos(ya), math.sin(za)*math.cos(ya), -math.sin(ya)],
         [math.sin(xa)*math.sin(ya)*math.cos(za)-math.sin(xa)*math.cos(xa), math.sin(xa)
         * math.sin(ya)*math.sin(za)+math.cos(xa)*math.cos(za), math.cos(ya)*math.sin(xa)],
         [math.cos(xa)*math.sin(ya)*math.cos(za)+math.sin(xa)*math.sin(za), math.cos(xa)*math.sin(ya)*math.sin(za)-math.sin(xa)*math.cos(za), math.cos(xa)*math.cos(ya)]]

    R = np.cross(T, U)
    return R, Xa


def calculateCoordinates(R, A):
    global vo1, ao1, vo, ao, xo, Af
    ax, ay, az = A
    X, Y, Z = R
    accel = ax*X+ay*Y+az*Z
    Ax, Ay, Az = accel          # in universal coordinate vectors
    vo = np.array([x*rr/2 for x in (ao+ao1)]+vo1)        #(ao+ao1)*rr/2 + vo1
    xf = np.array([x*pow(rr,2)/4 for x in (Af+ao)])+np.array([x*rr for x in vo])+np.array(xo)   #(Af+ao)*pow(rr, 2)/4+vo*rr+xo
    xo = np.array(xo)+np.array(xf)                # pass to plot.py if pressure>thresh
    vo1 = vo                    # updation
    ao1 = ao
    ao = Af


def write(coord):
    global arr
    arr=list(arr)
    arr.append(coord)
    refresh()


def cleararr():
    arr.clear()
    refresh()


def refresh():
    global arr
    if not we:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    arr=np.array(arr)
    coords=arr.astype(int)
    cv.polylines(canvas, [np.array(coords)], False, (0,0,255), 10)
    cv.imshow('image', canvas)


def plotPoints():
    global pThresh, P, xo
    if(P > pThresh):
        write(xo)
    else:
        cleararr()


if __name__ == "__main__":
    JSONRead('{"accX": 308, "accY": -164, "accZ": 1,"gyroX": -656, "gyroY": -415, "gyroZ": 110, "pressure": 1, "erase": 0}')
    i, j, k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    X = 0*i+0*j+0*k                                     # origin
    canvas = np.ones((1080, 1920))                      # defining the canvas
    R,Xa=changeCoordinateSystem(A, G, Xa)               # next line exists
    calculateCoordinates(R, A)
    plotPoints()
    time.sleep(rr)

    cv.imshow('image', canvas)
    cv.waitKey(0)
    cv.destroyAllWindows()
