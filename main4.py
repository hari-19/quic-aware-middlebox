#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI


class Host(Node):
    def config(self, **params):
        super(Host, self).config(**params)
        self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Host, self).terminate()


class NetworkTopo(Topo):
    def build(self, rlCount, natCount, **_opts):
        # Add 3 routers in three different subnets
        r1 = self.addHost('r1', cls=Host, ip='10.0.0.1/24')
        r2 = self.addHost('r2', cls=Host, ip='10.1.0.1/24')
        r3 = self.addHost('r3', cls=Host, ip='10.2.0.1/24')

        # Add 3 switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add host-switch links in the same subnet for each router
        self.addLink(s1, r1, intfName2='r1-eth1', params2={'ip': '10.0.0.1/24'})
        self.addLink(s2, r2, intfName2='r2-eth1', params2={'ip': '10.1.0.1/24'})
        self.addLink(s3, r3, intfName2='r3-eth1', params2={'ip': '10.2.0.1/24'})

        # Add router-router links for interconnection
        self.addLink(r1, r2, intfName1='r1-eth2', intfName2='r2-eth2', params1={'ip': '10.10.0.1/24'}, params2={'ip': '10.10.0.2/24'})
        self.addLink(r2, r3, intfName1='r2-eth3', intfName2='r3-eth3', params1={'ip': '10.30.0.2/24'}, params2={'ip': '10.30.0.3/24'})

        # Adding hosts specifying the default route
        client = self.addHost(name='client', ip='10.0.0.21/24', defaultRoute='via 10.0.0.1')
        server = self.addHost(name='server', ip='10.2.0.26/24', defaultRoute='via 10.2.0.1')
        # d2 = self.addHost(name='d2', ip='10.1.0.22/24', defaultRoute='via 10.1.0.1')
        # d3 = self.addHost(name='d3', ip='10.2.0.23/24', defaultRoute='via 10.2.0.1')
        # d4 = self.addHost(name='d4', ip='10.0.0.24/24', defaultRoute='via 10.0.0.1')
        # d5 = self.addHost(name='d5', ip='10.1.0.25/24', defaultRoute='via 10.1.0.1')

        # Add host-switch links
        self.addLink(client, s1)
        # self.addLink(d2, s2)
        # self.addLink(d3, s3)
        # self.addLink(d4, s1)
        # self.addLink(d5, s2)
        self.addLink(server, s3)


def run():
    topo = NetworkTopo(1, 1)
    net = Mininet(topo=topo)

    # Add routing for reaching networks that aren't directly connected
    info(net['r1'].cmd("ip route add 10.0.0.0/8 via 10.10.0.2"))
    info(net['r2'].cmd("ip route add 10.0.0.0/24 via 10.10.0.1"))
    info(net['r2'].cmd("ip route add 10.2.0.0/24 via 10.30.0.3"))
    info(net['r3'].cmd("ip route add 10.0.0.0/8 via 10.30.0.2"))


    net.start()
    CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()