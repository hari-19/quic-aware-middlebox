from mininet.log import setLogLevel, info
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import TCLink
import time
import os
from setup import TwoNATNetworkTopo, ThreeNATNetworkTopo, two_nat_ip_route, three_nat_ip_route, OneNetworkTopo, FourNATNetworkTopo, four_nat_ip_route, FiveNATNetworkTopo, five_nat_ip_route, OneNATNetworkTopo

def run_default_nat():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --NATTable --privateIp "10.0.0.1" --publicIp "192.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./misc/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./misc/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()


def run_default_rl():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].setMAC("66:e0:87:7d:d9:a4", intf="r1-eth1")
    net['r1'].setMAC("66:e0:87:7d:d9:b5", intf="r1-eth2")
    net['r1'].cmdPrint("./venv/bin/python3 ./default/rl.py > logs/rl.log &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./misc/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./misc/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()


def run_quic_nat_online():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --NATTable --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./misc/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./misc/client.py --host 192.168.1.100 --port 1000 -v")    
    net.stop()


def run_quic_nat_offline():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --NATTable --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./misc/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./misc/client.py --host 192.168.1.100 --port 1000 -v")    
    net.stop()


def run_quic_rl():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].setMAC("66:e0:87:7d:d9:a4", intf="r1-eth1")
    net['r1'].setMAC("66:e0:87:7d:d9:b5", intf="r1-eth2")
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint("./venv/bin/python3 ./online/rl.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./misc/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./misc/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()



def run_naive_nat_processing_time():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT_proc.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./processing_time/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    for i in range(1):
        net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    
    net.stop()


def run_quic_online_nat_processing_time():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT_proc.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./processing_time/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)

    for i in range(1):
        net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    
    net.stop()

def run_quic_offline_nat_processing_time():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT_proc.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./processing_time/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)

    for i in range(1):
        net["client"].cmdPrint("./venv/bin/python ./processing_time/client.py --host 192.168.1.100 --port 1000 -v")
    
    net.stop()

def run_nat_processing_time():
    os.system("rm -r processing_time_output")
    os.system("mkdir processing_time_output")
    os.system("rm default_cycles.txt")
    os.system("rm nat_online_cycles.txt")
    os.system("rm nat_offline_cycles.txt")

    print("Default NAT...")
    run_naive_nat_processing_time()
    os.system("mv default_cycles.txt processing_time_output/default_nat_processing_time.txt")
    print("QUIC NAT (Online)...")
    run_quic_online_nat_processing_time()
    os.system("mv nat_online_cycles.txt processing_time_output/quic_nat_online_processing_time.txt")
    print("QUIC NAT (Offline)...")
    run_quic_offline_nat_processing_time()
    os.system("mv nat_offline_cycles.txt processing_time_output/quic_nat_offline_processing_time.txt")
    

def run_default_nat_latency():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./latency/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./latency/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()

def run_quic_nat_online_latency():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./latency/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./latency/client.py --host 192.168.1.100 --port 1000 -v")
    
    net.stop()



def run_quic_nat_offline_latency():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
    time.sleep(1)
    net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    time.sleep(1)

    net["server"].cmdPrint("./venv/bin/python ./latency/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./latency/client.py --host 192.168.1.100 --port 1000 -v")
    
    net.stop()


def run_nat_latency():
    os.system("rm -r latency_output")
    os.system("rm latency_data.txt")
    os.system("rm default_latency.txt")
    os.system("rm nat_online_latency.txt")
    os.system("rm nat_offline_latency.txt")

    os.system("mkdir latency_output")

    print("Default NAT...")
    run_default_nat_latency()
    os.system("mv latency_data.txt latency_output/default_nat_latency.txt")
    print("QUIC NAT (Online)...")
    run_quic_nat_online_latency()
    os.system("mv latency_data.txt latency_output/quic_nat_online_latency.txt")
    print("QUIC NAT (Offline)...")
    run_quic_nat_offline_latency()
    os.system("mv latency_data.txt latency_output/quic_nat_offline_latency.txt")


def run_naive_nat_throughput():
    # topo = OneNetworkTopo()
    # topo = NATNetworkTopo()
    topo = OneNATNetworkTopo()
    # topo = TwoNATNetworkTopo()
    # topo = ThreeNATNetworkTopo()
    # topo = FourNATNetworkTopo()
    # topo = FiveNATNetworkTopo()
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

def run_throughput_zero_nat():
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net['r1'].setMAC("66:e0:87:7d:d9:a4", intf="r1-eth1")
    net['r1'].setMAC("66:e0:87:7d:d9:b5", intf="r1-eth2")
    net.start()
    net['r1'].cmdPrint('./venv/bin/python3 ./default/simple_forward.py --clientIp "10.0.0.1" --serverIp "192.168.1.1" --clientIface "r1-eth1" --serverIface "r1-eth2" --mac1 "66:e0:87:7d:d9:a4" --mac2 "66:e0:87:7d:d9:b5" &')
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")
    net.stop()


def run_throughput_one_nat(nat_type):
    topo = OneNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    
    match nat_type:
        case "default":
            net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
        case "online":
            net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
        case "offline":
            net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "10.0.0.1" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.0.0/24" &')
    
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")

    net.stop()

def run_throughput_two_nat(nat_type):
    topo = TwoNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    two_nat_ip_route(net)
    net.start()
   
    match nat_type:
        case "default":
            net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "172.168.1.2" --publicIp "192.168.1.1" --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
        case "online":
            net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "172.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
        case "offline":
            net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "172.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
    
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")

    net.stop()


def run_throughput_three_nat(nat_type):
    topo = ThreeNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    three_nat_ip_route(net)
    net.start()

    match nat_type:
        case "default":
            net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "90.168.1.2" --publicIp "192.168.1.1" --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24" &')
        case "online":
            net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "90.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24" &')

        case "offline":
            net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "90.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24" &')
    
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")

    net.stop()


def run_throughput_four_nat(nat_type):
    topo = FourNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    four_nat_ip_route(net)
    net.start()


    match nat_type:
        case "default":
            net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24"  &')
            net['r4'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "100.168.1.2" --publicIp "192.168.1.1" --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" &')
        case "online":
            net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24"  &')
            net['r4'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "100.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" &')

        case "offline":
            net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24"  &')
            net['r4'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "100.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" &')


    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")

    net.stop()

def run_throughput_five_nat(nat_type):
    topo = FiveNATNetworkTopo()
    net = Mininet(topo=topo, link=TCLink)
    five_nat_ip_route(net)
    net.start()

    match nat_type:
        case "default":
            net['r1'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24"  &')
            net['r4'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "100.168.1.2" --publicIp "110.168.1.1" --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" &')
            net['r5'].cmdPrint('./venv/bin/python3 ./default/default_NAT.py --privateIp "110.168.1.2" --publicIp "192.168.1.1" --privateIface "r5-eth1" --publicIface "r5-eth2" --privateSubnet "110.168.1.0/24" &')
        case "online":
            net['agent'].cmdPrint("./venv/bin/python3 ./online/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24"  &')
            net['r4'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "100.168.1.2" --publicIp "110.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" &')
            net['r5'].cmdPrint('./venv/bin/python3 ./online/quic_NAT.py --privateIp "110.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r5-eth1" --publicIface "r5-eth2" --privateSubnet "110.168.1.0/24" &')
        case "offline":
            net['agent'].cmdPrint("./venv/bin/python3 ./offline/agent.py &")
            net['r1'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "10.0.1.1" --publicIp "172.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r1-eth1" --publicIface "r1-eth2" --privateSubnet "10.0.1.0/24" &')
            net['r2'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "172.168.1.2" --publicIp "90.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r2-eth1" --publicIface "r2-eth2" --privateSubnet "172.168.1.0/24" &')
            net['r3'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "90.168.1.2" --publicIp "100.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r3-eth1" --publicIface "r3-eth2" --privateSubnet "90.168.1.0/24"  &')
            net['r4'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "100.168.1.2" --publicIp "110.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r4-eth1" --publicIface "r4-eth2" --privateSubnet "100.168.1.0/24" &')
            net['r5'].cmdPrint('./venv/bin/python3 ./offline/quic_NAT.py --privateIp "110.168.1.2" --publicIp "192.168.1.1" --agentIp "10.0.0.22" --agentPort 12001 --privateIface "r5-eth1" --publicIface "r5-eth2" --privateSubnet "110.168.1.0/24" &')

    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python ./throughput/server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python ./throughput/client.py --host 192.168.1.100 --port 1000 -v")

    net.stop()



def run_throughput_individual(number_of_nat, type_of_nat):
    if number_of_nat > 5 or number_of_nat < 0:
        print("Invalid number of NATs")
        return
    
    match number_of_nat:
        case 0:
            run_throughput_zero_nat()
        case 1:
            run_throughput_one_nat(type_of_nat)
        case 2:
            run_throughput_two_nat(type_of_nat)
        case 3:
            run_throughput_three_nat(type_of_nat)
        case 4:
            run_throughput_four_nat(type_of_nat)
        case 5:
            run_throughput_five_nat(type_of_nat)

def write_throughput_to_file(number, nat_type):
    with open('throughput_data.txt', 'r') as f:
        lines = f.readlines()

    with open('throughput_output/{}_{}'.format(number, nat_type), 'a') as f:
        f.writelines(lines)

    os.remove('throughput_data.txt')
        


def run_throughput():
    type_of_nat = ["default", "online", "offline"]
    os.system('rm -r throughput_output')
    os.system('mkdir throughput_output')
    os.system('rm throughput_data.txt')

    for i in range(10):
        print("Iteration {}".format(i))
        run_throughput_individual(0, "default")
        write_throughput_to_file(0, "default")
        for number in range(1, 6):
            for nat_type in type_of_nat:
                run_throughput_individual(number, nat_type)
                write_throughput_to_file(number, nat_type)


def get_choice():
    print("1. Run Emulation of Exiting Implementation using NAT")
    print("2. Run Emulation of Existing Implementation using RL")
    print("3. Run Emulation of Proposed Implementation using NAT (Online)")
    print("4. Run Emulation of Proposed Implementation using NAT (Offline)")
    print("5. Run Emulation of Proposed Implementation using RL (Online)")
    print("6. Evaluate NAT Processing Time")
    print("7. Evaluate Latency")
    print("8. Evaluate Throughput")
    return int(input("Enter you choice: "))

if __name__ == "__main__":
    setLogLevel('info')
    os.system("rm -r logs")
    # os.system("./venv/bin/pip3 install ./aioquic")

    os.mkdir("logs")
    c = get_choice()
    
    match c:
        case 1:
            run_default_nat()
        case 2:
            run_default_rl()
        case 3:
            run_quic_nat_online()
        case 4:
            run_quic_nat_offline()
        case 5:
            run_quic_rl()
        case 6:
            run_nat_processing_time()
        case 7:
            run_nat_latency()
        case 8:
            run_throughput()
        case _:
            print("Invalid choice")
