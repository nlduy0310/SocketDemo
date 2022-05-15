from base64 import encode
import socket
import os

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
SEPARATOR = "</>"
BUFFER_SIZE = 1024


# Receive a list from server
def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.appennd(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    return list

# Receive a file from server
def recvFile(conn):
    fileInfo = conn.recv(BUFFER_SIZE).decode(FORMAT)
    conn.sendall("ReadyToReceiveFile".encode(FORMAT))
    fileName, fileSize = fileInfo.split(SEPARATOR)
    fileName = ".\\Data\\" + os.path.basename(fileName)
    fileSize = int(fileSize)
    fileOut = open(fileName, "wb") 
    condition = 1   
    while (condition==1):
        # Receive 1024 bytes from the socket
        bytes_read = conn.recv(BUFFER_SIZE)
        if (len(bytes_read) < 1024):    # reach end of file
            if (len(bytes_read)==17 and bytes_read.decode(FORMAT)=="END_FILE_TRANSFER"):    # An end message in need
                break
            condition = 0
        # Write to the file the bytes we just received        
        fileOut.write(bytes_read)
    print("File is transfered.")
    fileOut.close()
    


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("CLIENT SIDE")

try:
    client.connect((HOST, SERVER_PORT))
    print("Client address: ", client.getsockname())

    msg = None
    while (msg != "x"):
        msg = input("Input: ")
        client.sendall(msg.encode(FORMAT))
        if (msg == "list"):
            list = recvList(client)
        elif (msg == "file"):
            recvFile(client)
except:
    print("Error occured.")


client.close()
