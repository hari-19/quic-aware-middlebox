import pickle
import socket

AGENT_IP = "10.0.0.22"
AGENT_PORT = 12001


def get_cid(peer_cid):
    cid = bytes.fromhex(peer_cid)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.sendto(cid, (AGENT_IP, AGENT_PORT))
        print("CID sent to configuration agent succefully")
        message, address = sock.recvfrom(1024)
        global_cid = message
        print(global_cid.hex())
    except Exception as e:
        print("Error sending CID to configuration agent")
        print(e)
    finally:
        sock.close()


get_cid("780b3d755a969501")