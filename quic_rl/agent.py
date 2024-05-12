import socket
import pickle
from threading import Thread
import os
import time
import datetime
import logging

logger = logging.getLogger("agent")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    filename="logs/agent.log",
    filemode="w"
)
# def print(*args):
#     with open("logs/agent_log.txt", "a") as f:
#         for arg in args:
#             f.write(str(arg) + " ")
#         f.write("\n")

class Mapping:
    data = {}

    def store(self, global_cid, new_cid):
        self.data[new_cid] = global_cid
        logging.info("Storing mapping: " + global_cid.hex() + " "+ new_cid.hex())
        # pass
    
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
    
def get_config_thread():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('', 12001))

    while True:
        message, address = server_socket.recvfrom(1024)
        logging.info("Received Request message: " + message.hex())
        global_cid = get_cid(message)
        
        if global_cid is not None:
            logging.info("Sending global_cid: " + global_cid.hex())
            server_socket.sendto(global_cid, address)
        else:
            logging.info("Sending None global_cid")
            server_socket.sendto(bytes(0), address)

def main():
    try:
        os.mkdir("logs")
    except FileExistsError:
        pass
    
    with open("logs/agent_log.txt", "w") as f:
        f.write("")

    thread1 = Thread(target=get_config_thread)
    thread2 = Thread(target=post_config_thread)
   
    def print_all_mappings():
        while True:
            mapping.print_all()
            time.sleep(0.1)
   
    # thread3 = Thread(target=print_all_mappings)

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