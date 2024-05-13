#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

class Host(Node):
    def config(self, **params):
        super(Host, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Host, self).terminate()

class CustomNetworkTopo(Topo):
    def build(self, rlCount, natCount,**_opts):
        
        client = self.addHost('client', ip='10.0.1.21/8')
        server = self.addHost('server', ip='10.0.4.22/8')

        rl = self.addHost('rl', cls=Host, ip='10.0.1.22/8')
        nat1 = self.addHost('nat1', cls=Host, ip='10.0.2.22/8')
        nat2 = self.addHost('nat2', cls=Host, ip='10.0.3.22/8')

        self.addLink(client, rl, intfName1='client-0', intfName2='rl-0', params2={'ip': '10.0.1.22/8'})
        self.addLink(rl, nat1, intfName1='rl-1', intfName2='nat1-0', params1={'ip': '10.0.2.21/8'}, params2={'ip': '10.0.2.22/8'})
        self.addLink(nat1, nat2, intfName1='nat1-1', intfName2='nat2-0', params1={'ip': '10.0.3.21/8'} ,params2={'ip': '10.0.3.22/8'})
        self.addLink(nat2, server, intfName1='nat2-1', intfName2='server-0', params1={'ip': '10.0.4.22/8'})