from mininet.log import setLogLevel, info
from naive.setup import NetworkTopo
from quic_nat.setup import NATNetworkTopo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import time
import os

def run_naive():
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['client'].cmdPrint("ip addr add 10.0.0.45 dev client-eth0")
    net['r1'].cmdPrint("./venv/bin/python3 ./naive/NAT.py &")
    time.sleep(1)
    # CLI(net)
    net["server"].cmdPrint("./venv/bin/python ./naive/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./naive/client.py --host 192.168.1.100 --port 1000 -v")
    # CLI(net)
    net.stop()


def run_quic_nat():
    topo = NATNetworkTopo()
    net = Mininet(topo=topo)
    net.start()
    net['client'].cmdPrint("ip addr add 10.0.0.45 dev client-eth0")
    net['r1'].cmdPrint("./venv/bin/python3 ./quic_nat/NAT.py &")
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 ./quic_nat/agent.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./quic_nat/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./quic_nat/client.py --host 192.168.1.100 --port 1000 -v")

    # CLI(net)
    net.stop()

def get_choice():
    print("1. Run Emulation of Exiting Implementation")
    print("2. Run Emulation of Proposed Implementation using NAT")
    return int(input("Enter your choice: "))

if __name__ == "__main__":
    setLogLevel('info')
    os.system("rm -r logs")
    # os.system("./venv/bin/pip3 install ./aioquic")
    c = get_choice()
    
    match c:
        case 1:
            run_naive()
        case 2:
            run_quic_nat()
        case _:
            print("Invalid choice")
