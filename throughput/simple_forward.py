import threading
import time
from scapy.all import *
import logging
import datetime
from quic_dissector import quic_dcid

import argparse

class SimpleFwdSniffer(threading.Thread):
    def __init__(self, input_iface, output_iface, logger, filter=None):
        super().__init__()
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
        
        if packet[Ether].src == MAC1 or packet[Ether].src == MAC2:
            return

        try:
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            src_port = packet[UDP].sport
            dst_port = packet[UDP].dport
            new_packet = IP(src=src_ip, dst=dst_ip) / UDP(sport=src_port, dport=dst_port) / packet[UDP].payload
            send(new_packet, iface=self.out_iface, verbose = False)
        
        except Exception as e:
            self.logger.error(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--clientIp', type=str, help='Client IP')
    parser.add_argument('--serverIp', type=str, help='Server IP')
    parser.add_argument('--clientIface', type=str, help='Client facing interface')
    parser.add_argument('--serverIface', type=str, help='Server facing interface')
    parser.add_argument('--mac1', type=str, help='MAC Address 1')
    parser.add_argument('--mac2', type=str, help='MAC Address 2')

    args = parser.parse_args()


    logger_client = logging.getLogger(args.clientIface)
    logger_server = logging.getLogger(args.serverIface)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s %(message)s",
        filename="logs/{}.log".format(args.clientIface),
        filemode="w"
    )

    CLIENT_FACING_IFACE = args.clientIface
    SERVER_FACING_IFACE = args.serverIface

    MAC1 = args.mac1
    MAC2 = args.mac2


    # Start a rate-limited sniffer
    in_sniffer = SimpleFwdSniffer(filter= "ip and (udp or tcp)",input_iface=CLIENT_FACING_IFACE, output_iface=SERVER_FACING_IFACE, logger=logger_client)
    in_sniffer.start()

    out_sniffer = SimpleFwdSniffer(filter="ip and (udp or tcp)", input_iface=SERVER_FACING_IFACE, output_iface=CLIENT_FACING_IFACE, logger=logger_server)
    out_sniffer.start()
