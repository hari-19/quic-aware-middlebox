import threading
import time
from scapy.all import *
import logging
import datetime

logger_client = logging.getLogger("rl-r1-eth1")
logger_server = logging.getLogger("rl-r1-eth2")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
    filename="logs/rl.log",
    filemode="w"
)

CLIENT_FACING_IFACE = "r1-eth1"
SERVER_FACING_IFACE = "r1-eth2"

CAPACITY = 100
REFILL_RATE = 5

class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.tokens = refill_rate
        self.refill_rate = refill_rate
        self.last_refill_time = time.time()

    def _refill(self):
        current_time = time.time()
        time_passed = current_time - self.last_refill_time
        tokens_to_add = int(time_passed * self.refill_rate)
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill_time = current_time

    def consume(self, tokens):
        # self._refill()
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        else:
            return False

class RateLimitedSniffer(threading.Thread):
    def __init__(self, token_buckets, filter=None, input_iface=CLIENT_FACING_IFACE, output_iface=SERVER_FACING_IFACE, logger=logger_client):
        super().__init__()
        self.token_buckets = token_buckets
        self.filter = filter
        self.in_iface = input_iface
        self.out_iface = output_iface
        self.logger = logger

    def run(self):
        self.logger.info("Starting sniffer...")
        sniff(iface=self.in_iface, filter=self.filter, prn=self.send_packet)

    def send_packet(self, packet):
        if not packet.haslayer(IP):
            return
        
        if packet[Ether].src == "66:e0:87:7d:d9:a4" or packet[Ether].src == "66:e0:87:7d:d9:b5":
            return

        try:
            self.logger.info(packet.summary())
            flow_id = self.get_flow_id(packet)
            self.logger.info(f"Flow ID: {flow_id}")
            token_bucket = self.token_buckets.get(flow_id)
            if token_bucket is None:
                self.logger.info("Creating new token bucket")
                token_bucket = TokenBucket(capacity=CAPACITY, refill_rate=REFILL_RATE)  # Default capacity and refill rate
                self.token_buckets[flow_id] = token_bucket
            
            if token_bucket.consume(1):  # Adjust tokens consumed per packet
                src_ip = packet[IP].src
                dst_ip = packet[IP].dst
                src_port = packet[UDP].sport
                dst_port = packet[UDP].dport
                new_packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / packet[UDP].payload
                send(new_packet, iface=self.out_iface, verbose = False)
                self.logger.info("Packet sent")
            else:
                self.logger.info("Dropping packet due to rate limiting")
        
        except Exception as e:
            self.logger.error(f"Error: {e}")

    def get_flow_id(self, packet):
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        return (src_ip, src_port, dst_ip, dst_port)

def print_token_bucket(token_buckets):
    with open("logs/RL_mappings.txt", "w") as f:
        now = datetime.datetime.now()
        f.write("Last Updated: "+ str(now) +"\n")
        f.write("No of mappings:" + str(len(token_buckets)) + "\n")
        bound_line = "-"*90
        line = "|{:^15} | {:^15} | {:^15} | {:^15} | {:^15} |".format("Src IP", "Src Port", "Dst IP", "Dst Port", "Tokens")
        f.write(bound_line + "\n")
        f.write(line + "\n")
        f.write(bound_line + "\n")
        for flow_id, token_bucket in token_buckets.items():
            line = "|{:^15} | {:^15} | {:^15} | {:^15} | {:^15} |".format(flow_id[0], flow_id[1], flow_id[2], flow_id[3], str(token_bucket.tokens))
            f.write(line + "\n")
            f.write(bound_line + "\n")

def refill_token_bucket(token_bucket):
    for flow_id, token_bucket in token_buckets.items():
        token_bucket._refill()

if __name__ == "__main__":
    # Create a dictionary to store token buckets for each flow
    token_buckets = {}

    # Start a rate-limited sniffer
    in_sniffer = RateLimitedSniffer(token_buckets, filter= "ip and (udp)",input_iface=CLIENT_FACING_IFACE, output_iface=SERVER_FACING_IFACE, logger=logger_client)
    in_sniffer.start()

    out_sniffer = RateLimitedSniffer(token_buckets, filter="ip and (udp or tcp)", input_iface=SERVER_FACING_IFACE, output_iface=CLIENT_FACING_IFACE, logger=logger_server)
    out_sniffer.start()

    def print_mapping_loop():
        while True:
            print_token_bucket(token_buckets)
            time.sleep(0.1)
    
    def refill_token_bucket_loop():
        while True:
            refill_token_bucket(token_buckets)
            time.sleep(1)

    thread1 = Thread(target=print_mapping_loop)
    thread1.start()

    thread2 = Thread(target=refill_token_bucket_loop)    
    thread2.start()
