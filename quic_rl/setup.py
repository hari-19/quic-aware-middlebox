#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

class QUICRLNetworkTopo(Topo):
    def build(self, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', ip=None)
        # Add 3 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        # Add host-switch links in the same subnet for each router
        self.addLink(s1, r1, intfName2='r1-eth1', params2={'ip': '10.0.0.1/24'})

        # Adding hosts specifying the default route
        d1 = self.addHost(name='client', ip='10.0.0.21/24', defaultRoute='via 10.0.0.1')
        d2 = self.addHost(name='agent', ip='10.0.0.22/24', defaultRoute='via 10.0.0.1')
        d3 = self.addHost(name='server', ip='192.168.1.100/24', defaultRoute='via 192.168.1.1')

        # Add host-switch links
        self.addLink(d1, s1)
        self.addLink(d2, s1)
        self.addLink(d3, s2, params1={'ip': '192.168.1.100/24'})
        self.addLink(s2, r1, intfName2='r1-eth2', params2={'ip': '192.168.1.1/24'})
