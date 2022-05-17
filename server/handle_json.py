import json

CLIENTS_FILE = "data/clients.json"

class Client:
    def __init__(self, data):
        self.id = data['id']
        self.fullname = data['fullname']
        self.contact = data['contact']
        self.email = data['email']
        self.bigAvatar = data['bigAvatar']
        self.smallAvatar = data['smallAvatar']
    def __str__(self):
        return "Id: " + str(client.id) + " \nFull name: " +  client.fullname + " \nContract: " +  client.contact + "\nEmail: " + client.email



# Load dữ liệu file json
def load():
    # Đọc file json:
    with open(CLIENTS_FILE, "r", encoding='utf-8') as read_file:
        data = json.load(read_file)
    clients = []
    # Lấy từng thành viên
    for client in data['clients']:
        clients.append(Client(client))
    
    # Sort theo ID
    clients.sort(key = lambda x: x.id)
    return clients

# Hàm lấy thuộc tính bigAvatar của người có id là idx
# getattr(clients[idx], 'bigAvatar')
# ------- main ------- #

if __name__ == "__main__":
    clients = load()
    for client in clients:
        print(client)
