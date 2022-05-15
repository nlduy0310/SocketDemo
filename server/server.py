import socket
from sys import argv
import threading
import os

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
SEPARATOR = "</>"
BUFFER_SIZE = 1024

# Send a list to client
def sendList(conn, list):
    for item in list:
        conn.sendall(item.encode(FORMAT))
        conn.recv(BUFFER_SIZE)
    endMsg = "end"
    conn.send(endMsg.encode(FORMAT))

# Send a file to client
def sendFile(conn, filename, filesize):
    conn.send(f"{filename}{SEPARATOR}{filesize}".encode(FORMAT))
    conn.recv(BUFFER_SIZE).decode(FORMAT)
    
    fileIn = open(filename, "rb")
    count = 0
    while(1):
        byte_read = fileIn.read(1024)
        conn.sendall(byte_read)
        count += 1
        if not byte_read:
            endMsg = "END_FILE_TRANSFER"
            conn.sendall(endMsg.encode(FORMAT))
            break      
    fileIn.close()         
              
# Handle with clients socket within threads
def handleClient(conn:socket, addr):
    print("Client ", addr, " connected")
    msg = None
    while (msg != "x"):
        msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
        print("Client ", addr, " said: ", msg)
        if (msg == "list"):
            list = []
            sendList(conn, list)

        elif (msg == "file"):
            sendFile(conn, "1.jpg", os.path.getsize("1.jpg"))
    print("Client ", addr, " finished, close", conn.getsockname())
    conn.close()


# ---main---
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, SERVER_PORT))
s.listen()

print("SERVER SIDE")
print("Server: ", HOST, SERVER_PORT)
print("Waiting for client")

nClient = 0
while(nClient < 3):
    try:
        conn, addr = s.accept()
        thread = threading.Thread(target=handleClient, args=(conn, addr))
        thread.daemon = False
        thread.start()
    except:
        print("Error occured.")
    nClient += 1

print("End")

s.close()
