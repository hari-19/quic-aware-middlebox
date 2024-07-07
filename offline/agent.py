import socket
import pickle
from threading import Thread
import os
import time
import datetime

def print(*args):
    with open("logs/agent_log.txt", "a") as f:
        for arg in args:
            f.write(str(arg) + " ")
        f.write("\n")

registered_middleboxes = {}

middlebox_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
middlebox_socket.bind(('', 12001))

class Mapping:
    data = {}

    def store(self, global_cid, new_cid):
        self.data[new_cid] = global_cid
    
    def get(self, new_cid):
        if new_cid in self.data.keys():
            return self.data[new_cid]
        
        return None

    def print_all(self):
        while True:
            with open("logs/agent_mappings.txt", "w") as f:
                now = datetime.datetime.now()
                f.write("Last Updated: "+ str(now) +"\n")
                f.write("No of mappings:" + str(len(self.data)) + "\n")
                bound_line = "-"*55
                line = "|{:^25} | {:^25} |".format("DCID", "GCID")
                f.write(bound_line + "\n")
                f.write(line + "\n")
                f.write(bound_line + "\n")
                for key, value in self.data.items():
                    line = "|{:^25} | {:^25} |".format(key.hex(), value.hex())
                    # f.write(bound_line + "\n")
                    f.write(line + "\n")
                    f.write(bound_line + "\n")
            time.sleep(0.1)

class Configuration:
    def __init__(self, original_cid, peer_cid):
        self.original_cid = original_cid
        self.peer_cid = peer_cid

def store_cid(message):
    data = pickle.loads(message)
    mapping.store(data.original_cid, data.peer_cid)
    
    for ip, port in registered_middleboxes[data.original_cid]:
        middlebox_socket.sendto(message, (ip, port))


def get_cid(message):
    cid = message
    global_cid = mapping.get(cid)
    return global_cid
    

def post_config_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12000))

    while True:
        message, address = server_socket.recvfrom(1024)
        store_cid(message)

def register_middlebox_thread():
    while True:
        message, address = middlebox_socket.recvfrom(1024)
        ip, port = address
        dcid = message

        print("Received Request message: ", message.hex())
        global_cid = get_cid(message)

        if global_cid is not None:
            print("Sending global_cid: ", global_cid.hex())
            data = Configuration(global_cid, dcid)
            serialized_obj = pickle.dumps(data)
            middlebox_socket.sendto(serialized_obj, address)
            if global_cid not in registered_middleboxes.keys():
                registered_middleboxes[global_cid] = [(ip, port)]
            else:
                registered_middleboxes[global_cid].append((ip, port))
        else:
            print("Sending None global_cid")
            data = Configuration(dcid, dcid)
            serialized_obj = pickle.dumps(data)
            middlebox_socket.sendto(serialized_obj, address)
            if dcid not in registered_middleboxes.keys():
                registered_middleboxes[dcid] = [(ip, port)]
            else:
                registered_middleboxes[dcid].append((ip, port))

# def get_config_thread():
#     server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     server_socket.bind(('', 12001))

#     while True:
#         message, address = server_socket.recvfrom(1024)
#         print("Received Request message: ", message.hex())
#         global_cid = get_cid(message)
        
#         if global_cid is not None:
#             print("Sending global_cid: ", global_cid.hex())
#             server_socket.sendto(global_cid, address)
#         else:
#             print("Sending None global_cid")
#             server_socket.sendto(bytes(0), address)

def main():
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass
    
    with open("logs/agent_log.txt", "w") as f:
        f.write("")

    thread1 = Thread(target=register_middlebox_thread)
    thread2 = Thread(target=post_config_thread)
   
    def print_all_mappings():
        while True:
            mapping.print_all()
            time.sleep(1)
   
    thread3 = Thread(target=print_all_mappings)

    print("Starting threads...")
    thread1.start()
    thread2.start()
    # thread3.start()
    thread1.join()
    thread2.join()
    # thread3.join()

if __name__ == "__main__":
    mapping = Mapping()
    main()