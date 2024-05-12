from mininet.log import setLogLevel, info
from naive_nat.setup import NetworkTopo
from quic_nat.setup import NATNetworkTopo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import time
import os
from naive_rl.setup import RLNetworkTopo

def run_naive_nat():
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['client'].cmdPrint("ip addr add 10.0.0.45 dev client-eth0")
    net['r1'].cmdPrint("./venv/bin/python3 ./naive_nat/NAT.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./naive_nat/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./naive_nat/client.py --host 192.168.1.100 --port 1000 -v")
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

def run_naive_rl():
    topo = RLNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].setMAC("66:e0:87:7d:d9:a4", intf="r1-eth1")
    net['r1'].setMAC("66:e0:87:7d:d9:b5", intf="r1-eth2")
    net['client'].cmdPrint("ip addr add 10.0.0.45 dev client-eth0")
    net["server"].cmdPrint("ip route add 10.0.0.0/24 via 192.168.1.1 dev server-eth0")
    # net["client"].cmdPrint("ip route add 192.168.0.0/16 via 10.0.0.1 dev client-eth0")
    net['r1'].cmdPrint("./venv/bin/python3 ./naive_rl/rl.py > logs/rl.log &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./naive_rl/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./naive_rl/client.py --host 192.168.1.100 --port 1000 -v")
    # CLI(net)

    net.stop()

def get_choice():
    print("1. Run Emulation of Exiting Implementation using NAT")
    print("2. Run Emulation of Proposed Implementation using NAT")
    print("3. Run Emulation of Existing Implementation using RL")
    return int(input("Enter your choice: "))
    # return 3

if __name__ == "__main__":
    setLogLevel('info')
    os.system("rm -r logs")
    # os.system("./venv/bin/pip3 install ./aioquic")

    os.mkdir("logs")
    c = get_choice()
    
    match c:
        case 1:
            run_naive_nat()
        case 2:
            run_quic_nat()
        case 3:
            run_naive_rl()
        case _:
            print("Invalid choice")
