from mininet.net import Mininet
from mininet.node import OVSSwitch, Controller
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.topo import Topo

from mininet.net import Mininet
from mininet.topo import Topo
from mininet.node import OVSSwitch, Controller
from mininet.log import setLogLevel

class MyTopology(Topo):
    def build(self, **kwargs):
        client = self.addHost('client')
        server = self.addHost('server')
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        switch1 = self.addSwitch('s1')
        switch2 = self.addSwitch('s2')

        self.addLink(client, switch1)
        self.addLink(h1, switch1)
        self.addLink(h1, h2)
        self.addLink(h2, switch2)
        self.addLink(server, switch2)

def create_network():
    topo = MyTopology()
    net = Mininet(topo=topo)
    net.start()
    
    # Assign IP addresses
    client, server, h1, h2 = net.get('client', 'server', 'h1', 'h2')
    client.setIP('192.168.1.1/24')
    server.setIP('192.168.1.4/24')
    h1.setIP('192.168.1.2/24', intf='h1-eth0')
    h1.setIP('192.168.2.1/24', intf='h1-eth1')
    h2.setIP('192.168.2.2/24', intf='h2-eth0')
    h2.setIP('192.168.1.3/24', intf='h2-eth1')

    # Enable IP forwarding on host 1 and host 2
    h1.cmd('sysctl -w net.ipv4.ip_forward=1')
    h2.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Set up routing on host 1 and host 2
    h1.cmd('ip route add 192.168.1.0/24 via 192.168.2.2')
    h2.cmd('ip route add 192.168.1.0/24 via 192.168.1.2')

    # Test connectivity
    # net.pingAll()
    CLI(net)

    # Stop Mininet
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    create_network()
