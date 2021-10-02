import numpy as numpy
import cv2 as cv

# vX, vY, L, B, lf=L/1080
# touch, pressure, ax, ay, x, y
# refresh rate :=> 1/acc

# [ax,ay,az,gx,gy,gz]-->A[Ax,Ay]->V[vx,vy]+D[dx,dy]
# [0,0]


def nextPoint():
    vo1 = [0, 0]
    ao1 = [0, 0]
    vo = [0, 0]
    xo = [0, 0]
    ao = [0, 0]
    rr = 0.1            # check refresh rate
    Af = [0, 0]

    while(1):
        vo = (ao+ao1)*rr/2 + vo1
        xf = (Af+ao)*pow(rr, 2)/4+vo*rr+xo
        xo = xo+xf  # pass to plot.py if pressure>thresh
        #xo1 = xo
        vo1 = vo
        ao1 = ao
        ao = Af
