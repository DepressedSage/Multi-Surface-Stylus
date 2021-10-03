import socket

HEADER = 64
# Sets the port for the connection
PORT = 5050
# Gets the IPv4 address of the SERVER side device
SERVER = socket.gethostbyname(socket.gethostname())
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNET"
ADDR = (SERVER, PORT)

socketClient= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketClient.bind(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msgLength = len(message)
    sendLength = str(msgLength).encode(FORMAT)
    sendLength += b' ' *(HEADER - len(sendLength))
    socketClient.send(sendLength)
    socketClient.send(message)
    print(socketClient.recv(2048).decode(FORMAT))

send("Hello World!")
input()
send("Hello Everyone!")
input()
send("Hello Tim!")

send(DISCONNECT_MESSAGE)
