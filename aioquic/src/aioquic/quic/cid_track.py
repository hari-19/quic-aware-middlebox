import pickle
import socket
import logging

logger = logging.getLogger("client")

AGENT_IP = "10.0.0.22"
AGENT_PORT = 12000

class Configuration:
    def __init__(self, original_cid, peer_cid):
        self.original_cid = original_cid
        self.peer_cid = peer_cid

def post_cid_config(global_cid, peer_cid):
    data = Configuration(global_cid, peer_cid)

    serialized_obj = pickle.dumps(data)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(serialized_obj, (AGENT_IP, AGENT_PORT))
        # print("CID sent to configuration agent succefully")
        # logger.info("CID sent to configuration agent succefully")
    except Exception as e:
        # print("Error sending CID to configuration agent")
        # logger.error("Error sending CID to configuration agent")
        print(e)
    finally:
        sock.close()