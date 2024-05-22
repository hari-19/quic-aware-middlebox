from mininet.log import setLogLevel, info
from naive_nat.setup import NetworkTopo
from quic_nat.setup import NATNetworkTopo
from quic_rl.setup import QUICRLNetworkTopo
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import time
import os
from naive_rl.setup import RLNetworkTopo
from throughput.setup import TwoNATNetworkTopo, ThreeNATNetworkTopo, two_nat_ip_route, three_nat_ip_route, OneNetworkTopo, FourNATNetworkTopo, four_nat_ip_route, FiveNATNetworkTopo, five_nat_ip_route, OneNATNetworkTopo

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

def run_quic_rl():
    topo = QUICRLNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].setMAC("66:e0:87:7d:d9:a4", intf="r1-eth1")
    net['r1'].setMAC("66:e0:87:7d:d9:b5", intf="r1-eth2")
    net['client'].cmdPrint("ip addr add 10.0.0.45 dev client-eth0")
    # net["server"].cmdPrint("ip route add 10.0.0.0/24 via 192.168.1.1 dev server-eth0")
    # net["client"].cmdPrint("ip route add 192.168.0.0/16 via 10.0.0.1 dev client-eth0")
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 ./quic_rl/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint("./venv/bin/python3 ./quic_rl/rl.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./quic_rl/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./quic_rl/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()

def run_naive_nat_processing_time():
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint("./venv/bin/python3 ./processing_time/NAT.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./processing_time/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    for i in range(10):
        net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()

def run_quic_nat_processing_time():
    topo = NATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint("./venv/bin/python3 ./processing_time/quic_NAT.py &")
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 ./quic_nat/agent.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./processing_time/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    # for i in range(10):
        # net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    
    for i in range(500):
        net["client"].cmdPrint("./venv/bin/python ./processing_time/client_dummy.py --host 192.168.1.100 --port 1000 -v")
    net.stop()

def run_quic_latency():
    topo = NATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint("./venv/bin/python3 ./latency/quic_NAT.py &")
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 ./quic_nat/agent.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./latency/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./latency/client.py --host 192.168.1.100 --port 1000 -v")
    
    # for i in range(10):
        # net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    
    # for i in range(500):
        # net["client"].cmdPrint("./venv/bin/python ./processing_time/client_dummy.py --host 192.168.1.100 --port 1000 -v")
    net.stop()


def run_quic_latency():
    topo = NetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint("./venv/bin/python3 ./latency/NAT.py &")
    time.sleep(1)
    # net['agent'].cmdPrint("./venv/bin/python3 ./quic_nat/agent.py &")
    # time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./latency/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./latency/client.py --host 192.168.1.100 --port 1000 -v")
    
    # for i in range(10):
        # net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    
    # for i in range(500):
        # net["client"].cmdPrint("./venv/bin/python ./processing_time/client_dummy.py --host 192.168.1.100 --port 1000 -v")
    net.stop()


def run_naive_nat_throughput():
    # topo = OneNetworkTopo()
    # topo = NATNetworkTopo()
    # topo = TwoNATNetworkTopo()
    # topo = ThreeNATNetworkTopo()
    # topo = FourNATNetworkTopo()
    # topo = FiveNATNetworkTopo()
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    # three_nat_ip_route(net)
    # two_nat_ip_route(net)
    # four_nat_ip_route(net)
    # five_nat_ip_route(net)
    net.start()
    # net['r1'].cmdPrint("./venv/bin/python3 ./quic_nat/NAT.py &")
    # # net['r1'].cmdPrint("./venv/bin/python3 ./naive_nat/NAT.py &")
    # time.sleep(1)
    # net['agent'].cmdPrint("./venv/bin/python3 ./quic_nat/agent.py &")
    # time.sleep(1)
    # net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    # time.sleep(1)
    # net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")
    
    # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" 

    # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" 
    # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "172.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" 

   # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" 
    # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" 
       # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "90.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24" 

   # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" 
    # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" 
       # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24" 
     #  ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "100.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" 


   # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" 
    # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" 
       # ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24" 
     #  ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "100.168.1.2" --publicIp "110.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" 
         #  ./venv/bin/python3 ./throughput/quic_NAT.py --privateIp "110.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r5-eth1" --publicIface "r5-eth2" --privateSubnet "110.168.1.0/24" 

    CLI(net)
    net.stop()

def get_choice():
    print("1. Run Emulation of Exiting Implementation using NAT")
    print("2. Run Emulation of Existing Implementation using RL")
    print("3. Run Emulation of Proposed Implementation using NAT")
    print("4. Run Emulation of Proposed Implementation using RL")
    # return int(input("Enter your choice: "))
    return 5

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
            run_naive_rl()
        case 3:
            run_quic_nat()
        case 4:
            run_quic_rl()
        case 5:
            run_naive_nat_throughput()
        case 6:
            run_naive_nat_processing_time()
        case 7:
            run_quic_nat_processing_time()
        case 8:
            run_quic_latency()
        case _:
            print("Invalid choice")
