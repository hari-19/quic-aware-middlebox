#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

class OneNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets


        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.1.21/24')
        d3 = self.addHost(name='server', ip='10.0.1.100/24')


        self.addLink(d1, d3)

class OneNATNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', ip=None)

        # Add 3 switches
        s1 = self.addSwitch('s1')

        # Add host-switch links in the same subnet for each router
        self.addLink(s1, r1, intfName2='r1-eth1', params2={'ip': '10.0.0.1/24'})

        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.0.21/24', defaultRoute='via 10.0.0.1')
        d2 = self.addHost(name='agent', ip='10.0.0.22/24', defaultRoute='via 10.0.0.1')
        d3 = self.addHost(name='server', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')

        # Add host-switch links
        self.addLink(d1, s1)
        self.addLink(d2, s1)
        self.addLink(d3, r1, intfName2='r1-eth2', params1={'ip': '192.168.1.100/24'}, params2={'ip': '192.168.1.1/24'})

class TwoNATNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', ip="10.0.1.1/24")
        r2 = self.addHost('r2', ip="172.168.1.2/24")

        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.1.21/24', defaultRoute='via 10.0.1.1')
        d2 = self.addHost(name='agent', ip='10.0.0.22/24')
        d3 = self.addHost(name='server', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')

        self.addLink(d1, r1, intfName2='r1-eth1', params2={'ip': '10.0.1.1/24'})
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', params1={'ip': '172.168.1.1/24'}, param2={'ip': '172.168.1.2/24'})
        self.addLink(r2, d3, intfName1='r2-eth2', params1={'ip': '192.168.1.1/24'})

        s1 = self.addSwitch('s1')

        self.addLink(d2, s1)
        self.addLink(d1, s1, intfName1='client-eth2', params1={'ip': '10.0.0.1/24'})
        self.addLink(r1, s1, intfName1='r1-eth3', params1={'ip': '10.0.0.2/24'})
        self.addLink(r2, s1, intfName1='r2-eth3', params1={'ip': '10.0.0.3/24'})

def two_nat_ip_route(net):
    net["r1"].cmdPrint("ip route add 192.168.1.0/24 via 172.168.1.2")
    net["r2"].cmdPrint("ip route add 10.0.1.0/24 via 172.168.1.1")


class ThreeNATNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', ip="10.0.1.1/24")
        r2 = self.addHost('r2', ip="172.168.1.2/24")
        r3 = self.addHost('r3', ip="90.168.1.2/24")

        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.1.21/24', defaultRoute='via 10.0.1.1')
        d2 = self.addHost(name='agent', ip='10.0.0.22/24')
        d3 = self.addHost(name='server', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')

        self.addLink(d1, r1, intfName2='r1-eth1', params2={'ip': '10.0.1.1/24'})
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', params1={'ip': '172.168.1.1/24'}, param2={'ip': '172.168.1.2/24'})
        self.addLink(r2, r3, intfName1='r2-eth2', params1={'ip': '90.168.1.1/24'}, intfName2='r3-eth1', params2={'ip': '90.168.1.2/24'})
        self.addLink(r3, d3, intfName1='r3-eth2', params1={'ip': '192.168.1.1/24'})

        s1 = self.addSwitch('s1')

        self.addLink(d2, s1)
        self.addLink(d1, s1, intfName1='client-eth2', params1={'ip': '10.0.0.1/24'})
        self.addLink(r1, s1, intfName1='r1-eth3', params1={'ip': '10.0.0.2/24'})
        self.addLink(r2, s1, intfName1='r2-eth3', params1={'ip': '10.0.0.3/24'})
        self.addLink(r3, s1, intfName1='r3-eth3', params1={'ip': '10.0.0.4/24'})


class FourNATNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', ip="10.0.1.1/24")
        r2 = self.addHost('r2', ip="172.168.1.2/24")
        r3 = self.addHost('r3', ip="90.168.1.2/24")
        r4 = self.addHost('r4', ip="100.168.1.2/24")

        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.1.21/24', defaultRoute='via 10.0.1.1')
        d2 = self.addHost(name='agent', ip='10.0.0.22/24')
        d3 = self.addHost(name='server', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')

        self.addLink(d1, r1, intfName2='r1-eth1', params2={'ip': '10.0.1.1/24'})
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', params1={'ip': '172.168.1.1/24'}, param2={'ip': '172.168.1.2/24'})
        self.addLink(r2, r3, intfName1='r2-eth2', params1={'ip': '90.168.1.1/24'}, intfName2='r3-eth1', params2={'ip': '90.168.1.2/24'})
        self.addLink(r3, r4, intfName1='r3-eth2', params1={'ip': '100.168.1.1/24'}, intfName2='r4-eth1', params2={'ip': '100.168.1.2/24'})
        self.addLink(r4, d3, intfName1='r4-eth2', params1={'ip': '192.168.1.1/24'})

        s1 = self.addSwitch('s1')

        self.addLink(d2, s1)
        self.addLink(d1, s1, intfName1='client-eth2', params1={'ip': '10.0.0.1/24'})
        self.addLink(r1, s1, intfName1='r1-eth3', params1={'ip': '10.0.0.2/24'})
        self.addLink(r2, s1, intfName1='r2-eth3', params1={'ip': '10.0.0.3/24'})
        self.addLink(r3, s1, intfName1='r3-eth3', params1={'ip': '10.0.0.4/24'})
        self.addLink(r4, s1, intfName1='r4-eth3', params1={'ip': '10.0.0.5/24'})

class FiveNATNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', ip="10.0.1.1/24")
        r2 = self.addHost('r2', ip="172.168.1.2/24")
        r3 = self.addHost('r3', ip="90.168.1.2/24")
        r4 = self.addHost('r4', ip="100.168.1.2/24")
        r5 = self.addHost('r5', ip="110.168.1.2/24")

        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.1.21/24', defaultRoute='via 10.0.1.1')
        d2 = self.addHost(name='agent', ip='10.0.0.22/24')
        d3 = self.addHost(name='server', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')

        self.addLink(d1, r1, intfName2='r1-eth1', params2={'ip': '10.0.1.1/24'})
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth1', params1={'ip': '172.168.1.1/24'}, param2={'ip': '172.168.1.2/24'})
        self.addLink(r2, r3, intfName1='r2-eth2', params1={'ip': '90.168.1.1/24'}, intfName2='r3-eth1', params2={'ip': '90.168.1.2/24'})
        self.addLink(r3, r4, intfName1='r3-eth2', params1={'ip': '100.168.1.1/24'}, intfName2='r4-eth1', params2={'ip': '100.168.1.2/24'})
        self.addLink(r4, r5, intfName1='r4-eth2', params1={'ip': '110.168.1.1/24'}, intfName2='r5-eth1', params2={'ip': '110.168.1.2/24'})
        self.addLink(r5, d3, intfName1='r5-eth2', params1={'ip': '192.168.1.1/24'})

        s1 = self.addSwitch('s1')

        self.addLink(d2, s1)
        self.addLink(d1, s1, intfName1='client-eth2', params1={'ip': '10.0.0.1/24'})
        self.addLink(r1, s1, intfName1='r1-eth3', params1={'ip': '10.0.0.2/24'})
        self.addLink(r2, s1, intfName1='r2-eth3', params1={'ip': '10.0.0.3/24'})
        self.addLink(r3, s1, intfName1='r3-eth3', params1={'ip': '10.0.0.4/24'})
        self.addLink(r4, s1, intfName1='r4-eth3', params1={'ip': '10.0.0.5/24'})
        self.addLink(r5, s1, intfName1='r5-eth3', params1={'ip': '10.0.0.6/24'})

def two_nat_ip_route(net):
    net["r1"].cmdPrint("ip route add 192.168.1.0/24 via 172.168.1.2")
    net["r2"].cmdPrint("ip route add 10.0.1.0/24 via 172.168.1.1")

def three_nat_ip_route(net):
    net["r1"].cmdPrint("ip route add 90.168.1.0/24 via 172.168.1.2")
    net["r1"].cmdPrint("ip route add 192.168.1.0/24 via 172.168.1.2")
    net["r2"].cmdPrint("ip route add 10.0.1.0/24 via 172.168.1.1")
    net["r2"].cmdPrint("ip route add 192.168.1.0/24 via 90.168.1.2")
    net["r3"].cmdPrint("ip route add 172.168.1.0/24 via 90.168.1.1")
    net["r3"].cmdPrint("ip route add 10.0.1.0/24 via 90.168.1.1")


def four_nat_ip_route(net):
    net["r1"].cmdPrint("ip route add 90.168.1.0/24 via 172.168.1.2")
    net["r1"].cmdPrint("ip route add 100.168.1.0/24 via 172.168.1.2")
    net["r1"].cmdPrint("ip route add 192.168.1.0/24 via 172.168.1.2")
    net["r2"].cmdPrint("ip route add 10.0.1.0/24 via 172.168.1.1")
    net["r2"].cmdPrint("ip route add 192.168.1.0/24 via 90.168.1.2")
    net["r2"].cmdPrint("ip route add 100.168.1.0/24 via 90.168.1.2")
    net["r3"].cmdPrint("ip route add 172.168.1.0/24 via 90.168.1.1")
    net["r3"].cmdPrint("ip route add 10.0.1.0/24 via 90.168.1.1")
    net["r3"].cmdPrint("ip route add 192.168.1.0/24 via 100.168.1.2")
    net["r4"].cmdPrint("ip route add 10.0.1.0/24 via 100.168.1.1")
    net["r4"].cmdPrint("ip route add 172.168.1.0/24 via 100.168.1.1")
    net["r4"].cmdPrint("ip route add 90.168.1.0/24 via 100.168.1.1")
    
def five_nat_ip_route(net):
    net["r1"].cmdPrint("ip route add 90.168.1.0/24 via 172.168.1.2")
    net["r1"].cmdPrint("ip route add 100.168.1.0/24 via 172.168.1.2")
    net["r1"].cmdPrint("ip route add 110.168.1.0/24 via 172.168.1.2")
    net["r1"].cmdPrint("ip route add 192.168.1.0/24 via 172.168.1.2")
    net["r2"].cmdPrint("ip route add 10.0.1.0/24 via 172.168.1.1")
    net["r2"].cmdPrint("ip route add 192.168.1.0/24 via 90.168.1.2")
    net["r2"].cmdPrint("ip route add 100.168.1.0/24 via 90.168.1.2")
    net["r2"].cmdPrint("ip route add 110.168.1.0/24 via 90.168.1.2")
    net["r3"].cmdPrint("ip route add 172.168.1.0/24 via 90.168.1.1")
    net["r3"].cmdPrint("ip route add 10.0.1.0/24 via 90.168.1.1")
    net["r3"].cmdPrint("ip route add 192.168.1.0/24 via 100.168.1.2")
    net["r3"].cmdPrint("ip route add 110.168.1.0/24 via 100.168.1.2")
    net["r4"].cmdPrint("ip route add 10.0.1.0/24 via 100.168.1.1")
    net["r4"].cmdPrint("ip route add 172.168.1.0/24 via 100.168.1.1")
    net["r4"].cmdPrint("ip route add 90.168.1.0/24 via 100.168.1.1")
    net["r4"].cmdPrint("ip route add 192.168.1.0/24 via 110.168.1.2")
    net["r5"].cmdPrint("ip route add 10.0.1.0/24 via 110.168.1.1")
    net["r5"].cmdPrint("ip route add 172.168.1.0/24 via 110.168.1.1")
    net["r5"].cmdPrint("ip route add 90.168.1.0/24 via 110.168.1.1")
    net["r5"].cmdPrint("ip route add 100.168.1.0/24 via 110.168.1.1")
    
