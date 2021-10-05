import socket
import threading

HEADER = 200
# Sets the port for the connection
PORT = 5050
# Gets the IPv4 address of the SERVER side device
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServer.bind(ADDR)

def handleClient(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        msgLength=len(msg)
        if msgLength:
           # msgLength = int(msgLength)
            msg = conn.recv(HEADER).decode(FORMAT)
            print(f"[{addr}] {msg}")
            print(len(msg))
            if msg == DISCONNECT_MESSAGE:
                connected = False

    print("Closing connection")
    conn.close()

def start():
    socketServer.listen()
    print("[LISTENING] Server is listening on", SERVER)
    while True:
        conn, addr = socketServer.accept()
        thread = threading.Thread(target = handleClient, args = (conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")

print("[STARTING] server is starting...")
start()

