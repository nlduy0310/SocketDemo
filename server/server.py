import socket
from sys import argv
import threading
import os
import handle_json as hj

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
SEPARATOR = "</>"
BUFFER_SIZE = 1024

# Send a list to client
def sendList(conn, list):
    for item in list:
        conn.sendall(str(item).encode(FORMAT))
        conn.recv(BUFFER_SIZE)
    endMsg = "end"
    conn.send(endMsg.encode(FORMAT))

# Send a file to client
def sendFile(conn, filename, filesize):
    print(f"{filename}{SEPARATOR}{filesize}")
    conn.send(f"{filename}{SEPARATOR}{filesize}".encode(FORMAT))
    conn.recv(BUFFER_SIZE).decode(FORMAT)
    
    fileIn = open(filename, "rb")
    count = 0
    while(1):
        byte_read = fileIn.read(1024)   
        if not byte_read:
            endMsg = "END_FILE_TRANSFER"
            # print('sending end message')
            conn.sendall(endMsg.encode(FORMAT))
            break
        conn.sendall(byte_read)
        # print('sending', len(byte_read))
        count += 1
             
    fileIn.close()         
              
# Handle with clients socket within threads
def handleClient(conn:socket, addr):
    print("Client ", addr, " connected")
    msg = None
    while (1):
        msg = conn.recv(BUFFER_SIZE).decode(FORMAT)
        print("Client ", addr, " said: ", msg)
        if (msg == "x"):
            break
        elif (msg == "close all"):
            global listening
            listening = 0
            endSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            endSock.connect((HOST, SERVER_PORT))
            endSock.close()
            break
        elif (msg == "big ava"):
            conn.send(msg.encode(FORMAT))
            id = conn.recv(BUFFER_SIZE).decode(FORMAT)
            id = int(id)
            path = clients.find_by_id(id).get_dir_big_avatar()
            sendFile(conn, path, os.path.getsize(path))
        elif (msg == "small ava"):
            conn.send(str(clients.size).encode(FORMAT))
            conn.recv(BUFFER_SIZE).decode(FORMAT)
            for i in range(clients.size):
                path = clients.client_list[i].get_dir_small_avatar()
                sendFile(conn, path, os.path.getsize(path))
                conn.recv(BUFFER_SIZE).decode(FORMAT)
        elif (msg == "list"):
            conn.send(str(clients.size).encode(FORMAT))
            conn.recv(BUFFER_SIZE).decode(FORMAT)
            for i in range(clients.size):
                member = [clients.client_list[i].id, clients.client_list[i].fullname, "null", "null"]
                sendList(conn, member)
                conn.recv(BUFFER_SIZE).decode(FORMAT)
        elif (msg == "info"):
            conn.send(msg.encode(FORMAT))
            id = conn.recv(BUFFER_SIZE).decode(FORMAT)
            id = int(id)
            info = [clients.client_list[id].contact, clients.client_list[id].email]
            sendList(conn, info)


        

    print("Client ", addr, " finished, close", conn.getsockname())
    conn.close()
    if (msg == "close all"):
        global s
        s.close()




# ---main---
if __name__ == "__main__":
    clients = hj.load()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, SERVER_PORT))
    s.listen()

    print("SERVER SIDE")
    print("Server: ", HOST, SERVER_PORT)
    print("Waiting for client")

    listening = 1
    while(listening == 1):
        try:
            conn, addr = s.accept()
            if (listening == 0):
                break
            thread = threading.Thread(target=handleClient, args=(conn, addr))
            thread.daemon = False
            thread.start()
        except:
            print("A thread ended.")

    print("End.")
    s.close()
