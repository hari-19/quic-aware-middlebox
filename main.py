#!/usr/bin/python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Node
from mininet.log import setLogLevel, info
from mininet.cli import CLI
import time

# class LinuxRouter(Node):
#     def config(self, **params):
#         super(LinuxRouter, self).config(**params)
#         self.cmd('sysctl net.ipv4.ip_forward=1')

#     def terminate(self):
#         self.cmd('sysctl net.ipv4.ip_forward=0')
#         super(LinuxRouter, self).terminate()


class NetworkTopo(Topo):
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


def run():
    topo = NetworkTopo()
    net = Mininet(topo=topo)
    net.start()
    net['client'].cmdPrint("ip addr add 10.0.0.45 dev client-eth0")
    net['r1'].cmd("./venv/bin/python3 NAT.py > nat_log.txt  &")
    time.sleep(1)
    net['agent'].cmdPrint("./venv/bin/python3 configuration_agent.py > agent_log.txt &")
    time.sleep(1)
    net["server"].cmdPrint("./venv/bin/python server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 > client_log.txt &")
    time.sleep(1)
    net["client"].cmdPrint("./venv/bin/python client.py --host 192.168.1.100 --port 1000 -v > server_log.txt")

    # CLI(net)
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    run()
