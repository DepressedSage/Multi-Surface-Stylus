import socket
import time
import numpy as np
import json
import cv2 as cv
import math
from screeninfo import get_monitors

# defining required variables
rr = 1                     # refresh rate
Xa = np.array([0, 0, 0])     # Angles of XYZ wrt ijk
ao1 = np.array([0, 0])       # last to last acceleration
vo1 = np.array([0, 0])       # last to last velocity vector
ao = np.array([0, 0])        # last acceleration
vo = np.array([0, 0])        # last velocity vector
xo = np.array([0, 0])        # last coordinate
Af = np.array([0, 0])        # current acceleration
we = False                   # whether to write or erase
pThresh = 0.1                # pressure threshold for activation
arr = []                     # array to store points till plotting
A = np.array([0, 0, 0])      # acceleration vector
G = np.array([0, 0, 0])      # gyroscopic readings
P = 1                        # pressure
R = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
canvas = np.ones((1080, 1920)) 


def JSONRead(JSONstr):
    global A, G, P, we,Xa,R,canvas
    readings = json.loads(JSONstr)

    ax = readings["accX"]*10/16000 - 3
    ay = readings["accY"]*10/165 + 7
    az = readings["accZ"]*10/162 - 6.8
    gx = (readings["gyroX"])/100
    gy = (readings["gyroY"])*180/5500
    gz = (readings["gyroZ"])*180/800
    P = readings["pressure"]
    we = readings["erase"]
    print("ax\t",ax,"\tay\t",ay,"\taz\t",az,"gx\t",gx,"\tgy\t",gy,"\tgz\t",gz)
    A = np.array([ax, ay, az])
    G = np.array([gx, gy, gz])
    changeCoordinateSystem()
    calculateCoordinates(R, A)
    plotPoints()
    #cv.waitKey(0)
    #time.sleep(rr)
    P=1


def getAngle(x, g):
    x = x+g*rr
    return x


def changeCoordinateSystem():
    global R,Xa,A
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

    T = [[math.cos(math.radians(za))*math.cos(math.radians(ya)), math.sin(math.radians(za))*math.cos(math.radians(ya)), -math.sin(math.radians(ya))],
         [math.sin(math.radians(xa))*math.sin(math.radians(ya))*math.cos(math.radians(za))-math.sin(math.radians(xa))*math.cos(math.radians(xa)), math.sin(math.radians(xa))
         * math.sin(math.radians(ya))*math.sin(math.radians(za))+math.cos(math.radians(xa))*math.cos(math.radians(za)), math.cos(math.radians(ya))*math.sin(math.radians(xa))],
         [math.cos(math.radians(xa))*math.sin(math.radians(ya))*math.cos(math.radians(za))+math.sin(math.radians(xa))*math.sin(math.radians(za)), math.cos(math.radians(xa))*math.sin(math.radians(ya))*math.sin(math.radians(za))-math.sin(math.radians(xa))*math.cos(math.radians(za)), math.cos(math.radians(xa))*math.cos(math.radians(ya))]]

    R = np.cross(T, U)/np.linalg.norm(T)
    Xa=(xa,ya,za)


def calculateCoordinates(R, A):
    global vo1, ao1, vo, ao, xo, Af
    ax, ay, az = A
    X, Y, Z = R
    accel = (np.array(ax)*np.array(X)+np.array(ay)*np.array(Y)+np.array(az)*np.array(Z))/10
    Ax, Ay, Az = accel          # in universal coordinate vectors
    Af=[Ax,Ay]
    vo = np.array([x*rr/2 for x in (np.array(ao)+np.array(ao1))]+np.array(vo1))        #(ao+ao1)*rr/2 + vo1
    xf = np.array([x*pow(rr,2)/4 for x in (np.array(Af)+np.array(ao))])+np.array([x*rr for x in vo])+np.array(xo)   #(Af+ao)*pow(rr, 2)/4+vo*rr+xo
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
    global arr
    arr=np.array([])
    refresh()


def refresh():
    global arr
    if not we:
        color = (0, 0, 0)
    else:
        color = (255, 255, 255)
    arr=np.array(arr)
    coords=arr.astype(int)
    cv.polylines(canvas, [np.abs(np.array(coords))], False, (0,0,255), 10)
    cv.imshow('image', canvas)


def plotPoints():
    global pThresh, P, xo
    if(True):#P > pThresh):
        write(xo)
    else:
        cleararr()





def server_program():
    # get the hostname
    host = socket.gethostname()
    port = 5050  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    i=0
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(143).decode()
        data=data[data.index("\'")+1:]
        if "\'" in data:
            data=data[:data.index("\'")]
        if not data or data=="" :
            # if data is not received break
            
            break
        # do stuff with data
        JSONRead(data)
        
        # send someting back to client
        #my_client_data = my_application_function_that_returns_string()
        #conn.send(my_client_code.encode())  # send data to the client
        cv.waitKey(1)
    cv.destroyAllWindows()
    conn.close()  # close the connection



if __name__ == "__main__":
    #JSONRead('{"accX": 308, "accY": -164, "accZ": 1,"gyroX": -656, "gyroY": -415, "gyroZ": 110, "pressure": 1, "erase": 0}')
    #cv.imshow('image', canvas)
    server_program()

    i, j, k = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    X = 0*i+0*j+0*k                                     # origin
    #canvas = np.ones((1080, 1920))                      # defining the canvas
    #R,Xa=changeCoordinateSystem(A, G, Xa)               # next line exists
    #calculateCoordinates(R, A)
    #plotPoints()
    #time.sleep(rr)

    
    #cv.waitKey(0)
    cv.destroyAllWindows()
    cv.waitKey(1)