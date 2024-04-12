import socket
import pickle
from threading import Thread

class Mapping:
    data = {}

    def store(self, global_cid, new_cid):
        self.data[new_cid] = global_cid
    
    def get(self, new_cid):
        if new_cid in self.data.keys():
            return self.data[new_cid]
        
        return None

    def print_all(self):
        print("Printing all mappings...")
        for key, value in self.data.items():
            print(key.hex()," : " ,value.hex())
        print("End of mappings")

class Configuration:
    def __init__(self, original_cid, peer_cid):
        self.original_cid = original_cid
        self.peer_cid = peer_cid

def store_cid(message):
    data = pickle.loads(message)
    mapping.store(data.original_cid, data.peer_cid)

def get_cid(message):
    cid = message
    global_cid = mapping.get(cid)
    return global_cid
    

def post_config_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12000))

    while True:
        mapping.print_all()
        message, address = server_socket.recvfrom(1024)
        store_cid(message)
    
def get_config_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12001))

    while True:
        message, address = server_socket.recvfrom(1024)
        global_cid = get_cid(message)
        
        if global_cid is not None:
            server_socket.sendto(global_cid, address)
        else:
            server_socket.sendto(bytes(0), address)

def main():
    thread1 = Thread(target=get_config_thread)
    thread2 = Thread(target=post_config_thread)

    print("Starting threads...")
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

if __name__ == "__main__":
    mapping = Mapping()
    main()