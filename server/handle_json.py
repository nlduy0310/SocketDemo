import json
from PIL import Image, ImageOps, ImageDraw

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
            self.id = data['id']
            self.fullname = data['fullname']
            self.contact = data['contact']
            if isinstance(data['email'], type(None)):
                self.email = "null"
            else:
                self.email = data['email']

    def __str__(self):
        return "Id: " + str(self.id) + " \nFull name: " +  self.fullname + " \nContract: " +  self.contact + "\nEmail: " + self.email

    def get_dir_big_avatar(self):
        return DIRECT_TO_AVATAR[0] + str(self.id) + ".png"

    def get_dir_small_avatar(self):
        return DIRECT_TO_AVATAR[1] + str(self.id) + ".png"

# Danh sách client
class ClientList:

    def __init__(self, clients):
        self.client_list = clients
        self.size = len(clients)
        
    def show_all(self):
        for client in self.client_list:
            print(client)
    
    def find_by_id(self, idx):
        return self.client_list[idx] if idx < self.size and idx > 0 else Client(None)

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
        
        clients_res = [client for client in self.client_list if name.strip().lower() in client.fullname.lower()]

        clients_res = ClientList(clients_res)
        return clients_res
    
    # Hàm chuyển đổi sang avatar nhỏ
    def convert_big_to_small(self):
        size = (50, 50)
        for i in range(self.size):
            mask = Image.new('L', size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + size, fill=255)

            im = Image.open(self.client_list[i].get_dir_big_avatar())

            output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
            output.putalpha(mask)
            output.save(self.client_list[i].get_dir_small_avatar())


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
    clients.sort(key = lambda x: x.id)
    list_client = ClientList(clients)
    #print("size: ", len(clients))
    return list_client



# ------- main ------- #
if __name__ == "__main__":
    clients = load()
    # Hàm covert Avatar lớn sang nhỏ:
    clients.convert_big_to_small()
    # print("Tổng số thành viên: ", clients.size)
    # print("Thông tin thành viên: \n")
    # clients.show_all()  
    # print("\n")

    # Tìm theo id
    # print("Thành viên có id thứ 4:")
    # print(clients.find_by_id(4))
    # print("Thành viên thứ 15: ")
    # print(clients.find_by_id(15))

    # Tìm theo sdt:
    # print(clients.find_by_phone("0123456777"))
    # print(clients.find_by_phone("31231412312"))

    # Tim theo ten:
    # print("Tìm tên Phú: ")
    # list_by_name = clients.find_by_name("phú")
    # list_by_name.show_all()
    
    # print("Tìm tên có Nguyễn Văn: ")
    # list_by_name = clients.find_by_name("Nguyễn Văn")
    # list_by_name.show_all()

    # print("Tìm tên có họ Nguyễn: ")
    # list_by_name = clients.find_by_name("  Nguyễn   ")
    # list_by_name.show_all()
 