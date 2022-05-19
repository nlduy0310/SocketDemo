from imp import load_package
import json
from PIL import Image, ImageOps, ImageDraw

page_size = 5
CLIENTS_FILE = "data/clients.json"
DIRECT_TO_AVATAR = []


class Client:

    def __init__(self, data):
        if(isinstance(data, type(None))):
            self.id = "null"
            self.fullname = "null"
            self.contact = "null"
            self.email = "null"

        else:
            self.id = str(data[0])
            self.fullname = str(data[1])
            self.contact = str(data[2])
            if isinstance(data[3], type(None)):
                self.email = "null"
            else:
                self.email = str(data[3])

    def __str__(self):
        return "Id: " + str(self.id) + " \nFull name: " + self.fullname + " \nContract: " + self.contact + "\nEmail: " + self.email

    def get_dir_big_avatar(self):
        return "data/avatar/big/" + str(self.id) + ".png"

    def get_dir_small_avatar(self):
        return "data/avatar/small/" + str(self.id) + ".png"

    def is_valid(self):
        return self.id != "null" and self.fullname != "null"

# Danh sách client


class ClientList:

    def __init__(self, clients):
        self.client_list = clients
        self.size = len(clients)
        self.cur_page = 1

    def show_all(self):
        for client in self.client_list:
            print(client)

    def find_by_id(self, id):
        for item in self.client_list:
            if item.id == id:
                return item

        return Client(None)

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

    def get_pages_count(self):
        if len(self.client_list) == 0:
            return 0
        elif (len(self.client_list) % page_size) == 0:
            return len(self.client_list) // page_size
        else:
            return int(self.client_list // page_size) + 1

    def load_client(self, page, index):

        if page < 1 or page > self.get_pages_count() or index < 0 or index >= page_size:
            return Client(None)
        else:
            return self.client_list[(page - 1) * page_size + index]

    def load_page(self, page):
        res = []
        for i in range(page_size):
            res.append(self.load_client(page, i))

        return res

    def next_page(self):
        if self.cur_page == self.get_pages_count():
            return self.load_page(self.cur_page)
        else:
            self.cur_page += 1
            return self.load_page(self.cur_page)

    def prev_page(self):
        if self.cur_page == 1:
            return self.load_page(self.cur_page)
        else:
            self.cur_page -= 1
            return self.load_page(self.cur_page)

    # Hàm chuyển đổi sang avatar nhỏ


# CÁC HÀM ĐỌC, HỖ TRỢ
# Load dữ liệu file json
def load():
    # Đọc file json:
    with open(CLIENTS_FILE, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)

    # Đường dẫn tới avatar, lớn index là 0, nhỏ: 1
    DIRECT_TO_AVATAR.append(data["direct_to_avatar"][0]["bigAvatar"])
    DIRECT_TO_AVATAR.append(data["direct_to_avatar"][0]["smallAvatar"])

    # Lấy từng thành viên
    clients = []
    for client in data['clients']:
        clients.append(Client(client))

    # Sort theo ID
    clients.sort(key=lambda x: x.id)
    list_client = ClientList(clients)
    return list_client
