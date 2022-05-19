from base64 import encode
import socket
import traceback
import os

HOST = "127.0.0.1"
SERVER_PORT = 65432
FORMAT = "utf8"
SEPARATOR = "</>"
BUFFER_SIZE = 1024
END_MESSAGE_SIZE = 17


# Receive a list from server
def recvList(conn):
    list = []
    item = conn.recv(1024).decode(FORMAT)
    while(item != "end"):
        list.append(item)
        conn.sendall(item.encode(FORMAT))
        item = conn.recv(1024).decode(FORMAT)
    return list

# Receive a file from server


def recvFile(conn):
    fileInfo = conn.recv(BUFFER_SIZE).decode(FORMAT)
    conn.sendall("ReadyToReceiveFile".encode(FORMAT))
    fileName, fileSize = fileInfo.split(SEPARATOR)
    #fileName = ".\\data\\" + os.path.basename(fileName)
    fileSize = int(fileSize)
    bytes_count = 0
    fileOut = open(fileName, "wb")
    condition = 1
    while (condition == 1):
        # Receive 1024 bytes from the socket
        bytes_read = conn.recv(BUFFER_SIZE)
        bytes_count += len(bytes_read)
        # print('---', len(bytes_read), 'total:', bytes_count)

        # if (len(bytes_read) < 1024):    # reach end of file

        #     if (len(bytes_read) == 17 and bytes_read.decode(FORMAT) == "END_FILE_TRANSFER"):
        #         print('EFT')    # An end message in need
        #         break
        #     condition = 0

        if bytes_count < fileSize:
            fileOut.write(bytes_read)
            # print('writing', len(bytes_read))
        elif bytes_count == fileSize:
            bytes_read = conn.recv(BUFFER_SIZE)  # end message
            fileOut.write(bytes_read)
            break
        else:
            diff = bytes_count - fileSize
            if diff == 17:
                fileOut.write(bytes_read[:-END_MESSAGE_SIZE])
            else:
                fileOut.write(bytes_read[:-diff])
                bytes_read = conn.recv(BUFFER_SIZE)
            break

        # Write to the file the bytes we just received
        # fileOut.write(bytes_read)
    print("File is transfered.")
    fileOut.close()
    return fileName


class Client:

    def __init__(self, data):
        if(isinstance(data, type(None))):
            self.id = "null"
            self.fullname = "null"
            self.contact = "null"
            self.email = "null"

        else:
            self.id = data[0]
            self.fullname = data[1]
            self.contact = data[2]
            if isinstance(data[3], type(None)):
                self.email = "null"
            else:
                self.email = data[3]

    def __str__(self):
        return "Id: " + str(self.id) + " \nFull name: " + self.fullname + " \nContact: " + self.contact + "\nEmail: " + self.email


class ClientList:

    def __init__(self, clients):
        self.client_list = clients
        self.size = len(clients)

    def show_all(self):
        for client in self.client_list:
            print(client)

    def find_by_id(self, idx):
        return self.client_list[idx] if idx < self.size and idx >= 0 else Client(None)

    def find_by_phone(self, phone):

        if(isinstance(phone, type(str)) != True):
            phone = str(phone)

        for i in range(self.size):
            if self.client_list[i].contact == phone:
                return self.client_list[i]

        return Client(None)

    def find_by_name(self, name):

        if(isinstance(name, type(str)) != True):
            name = str(name)

        clients_res = [client for client in self.client_list if name.strip(
        ).lower() in client.fullname.lower()]

        clients_res = ClientList(clients_res)
        return clients_res


# ---main---
if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("CLIENT SIDE")
    members = []
    list = ClientList(members)
    try:
        client.connect((HOST, SERVER_PORT))
        print("Client address: ", client.getsockname())

        msg = None
        while (msg != "x" and msg != "close all"):
            msg = input("Input: ")
            client.sendall(msg.encode(FORMAT))
            # Truy van danh sach ban dau
            if (msg == "list"):
                num = int(client.recv(BUFFER_SIZE).decode(FORMAT))
                client.send(msg.encode(FORMAT))
                for i in range(num):
                    memInfo = recvList(client)
                    mem = Client(memInfo)
                    members.append(mem)
                    client.send(msg.encode(FORMAT))
                list = ClientList(members)
            # Truy van Big avatar cho mot thanh vien
            elif (msg == "big ava"):
                client.recv(BUFFER_SIZE)
                id = 0  # ID cua thanh vien can lay thong tin
                client.send(str(id).encode(FORMAT))
                members[id].bigAvaPath = recvFile(client)
            # Truy van Small avatar cho tat ca thanh vien
            elif (msg == "small ava"):
                num = int(client.recv(BUFFER_SIZE).decode(FORMAT))
                client.send(msg.encode(FORMAT))
                for i in range(num):
                    members[i].smallAvaPath = recvFile(client)
                    client.send(msg.encode(FORMAT))
            # Truy van thong tin cu the cho mot thanh vien
            elif (msg == "info"):
                client.recv(BUFFER_SIZE)
                id = 0  # ID cua thanh vien can lay thong tin
                client.send(str(id).encode(FORMAT))
                addInfo = recvList(client)
                members[id].contact = addInfo[0]
                members[id].email = addInfo[1]

    except Exception:
        print("Error occured.")
        traceback.print_exception()

    list.show_all()
    client.close()
