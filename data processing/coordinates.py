import numpy as np
rr=0.1
def getAngle(x,g):
    x=x+g*rr
    return x
# [ax,ay,az,gx,gy,gz]-->A[Ax,Ay]->V[vx,vy]+D[dx,dy]

ax,ay,az=0,0,0
gx,gy,gz=0,0,0
x,y,z=0,0,0

x=getAngle(x,gx)
y=getAngle(y,gy)
z=getAngle(z,gz)

# list of universal coordinate unit vectors
U = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# list of relative coordinate unit vectors wrt MPU
R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

# [                   cos(z)cos(y),                    sin(z)cos(y),      -sin(y)]         # transformation matrix for R->U
# [sin(x)sin(y)cos(z)-sin(x)cos(x), sin(x)sin(y)sin(z)+cos(x)cos(z), cos(y)sin(x)]         # cross multiply with U to get R in terms of U
# [cos(x)sin(y)cos(z)+sin(x)sin(z), cos(x)sin(y)sin(z)-sin(x)cos(z), cos(x)cos(y)]         # x,y,z are angular displacements in their respective axes

ax, ay, az = (0, 0, 0)
gx, gy, gz = (0, 0, 0)
