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
        # self.cmd('sysctl net.ipv4.ip_forward=1')

    def terminate(self):
        # self.cmd('sysctl net.ipv4.ip_forward=0')
        super(Host, self).terminate()


class NetworkTopo(Topo):
    def build(self, rlCount, natCount, **_opts):
        # Add 3 routers in three different subnets

        client = self.addHost('client', ip='10.0.0.2/31', defaultRoute='via 10.0.0.3')

        serverIp = (rlCount + natCount)*2 + 3
        server = self.addHost('server', ip='10.0.0.{}/31'.format(serverIp), defaultRoute='via 10.0.0.{}'.format(serverIp - 1))

        rls = []
        nats = []

        for i in range(rlCount):
            rl = self.addHost('rl{}'.format(i), cls=Host, ip='10.0.0.{}/31'.format(i*2 + 3))
            rls.append(rl)
        
        for i in range(natCount):
            nat = self.addHost('nat{}'.format(i), cls=Host, ip='10.0.0.{}/31'.format((i + rlCount)*2 + 3))
            nats.append(nat)

        if rlCount > 0:
            self.addLink(client, rls[0], intfName1='client-0', intfName2='rl0-0', params2={'ip': '10.0.0.3/31'})
        elif natCount > 0:
            self.addLink(client, nats[0], intfName1='client-0', intfName2='nat0-0', params2={'ip': '10.0.0.3/31'})
        else:
            self.addLink(client, server, intfName1='client-0', intfName2='server-0', params2={'ip': '10.0.0.3/31'})    

        for i in range(1, rlCount):
            self.addLink(rls[i - 1], rls[i], intfName1='rl{}-1'.format(i - 1), intfName2='rl{}-0'.format(i), params1={'ip': '10.0.0.{}/31'.format(i*2 + 2)}, params2= {'ip': '10.0.0.{}/31'.format(i*2 + 3)})
        
        if rlCount > 0 and natCount > 0:
            self.addLink(rls[-1], nats[0], intfName1='rl{}-1'.format(rlCount - 1), intfName2='nat0-0', params1={'ip': '10.0.0.{}/31'.format((rlCount)*2 + 2)})

        for i in range(1, natCount):
            self.addLink(nats[i - 1], nats[i], intfName1='nat{}-1'.format(i - 1), intfName2='nat{}-0'.format(i), params1={'ip': '10.0.0.{}/31'.format((i + rlCount)*2 + 2)}, params2= {'ip': '10.0.0.{}/31'.format((i + rlCount)*2 + 3)})

        if natCount > 0:
            self.addLink(nats[-1], server, intfName1='nat{}-1'.format(natCount - 1), intfName2='server-0', params1={'ip': '10.0.0.{}/31'.format(serverIp - 1)})
        elif rlCount > 0:
            self.addLink(rls[-1], server, intfName1='rl{}-1'.format(rlCount - 1), intfName2='server-0', params1={'ip': '10.0.0.{}/31'.format(serverIp - 1)})


def run():

    rlCount = 0
    natCount = 1


    AGENT_IP = "10.0.0.22"
    AGENT_PORT = 12001

    topo = NetworkTopo(rlCount, natCount)
    net = Mininet(topo=topo)


    for i in range(0, rlCount):
        if i < 9:
            net['rl{}'.format(i)].setMAC('00:00:00:00:00:0{}'.format(i+1), intf='rl{}-0'.format(i))
            net['rl{}'.format(i)].setMAC('00:00:00:00:11:0{}'.format(i+1), intf='rl{}-1'.format(i))
        else:
            net['rl{}'.format(i)].setMAC('00:00:00:00:00:{}'.format(i+1), intf='rl{}-0'.format(i))
            net['rl{}'.format(i)].setMAC('00:00:00:00:11:{}'.format(i+1), intf='rl{}-1'.format(i))

    for i in range(0, natCount):
        if i < 9:
            net['nat{}'.format(i)].setMAC('00:00:00:22:00:0{}'.format(i+1), intf='nat{}-0'.format(i))
            net['nat{}'.format(i)].setMAC('00:00:00:22:11:0{}'.format(i+1), intf='nat{}-1'.format(i))
        else:
            net['nat{}'.format(i)].setMAC('00:00:00:22:00:{}'.format(i+1), intf='nat{}-0'.format(i))
            net['nat{}'.format(i)].setMAC('00:00:00:22:11:{}'.format(i+1), intf='nat{}-1'.format(i))


    net.start()
    for i in range(natCount):
        for j in range(i+1, natCount):
            print('nat{}'.format(i), "ip route add 10.0.0.{}/31 via 10.0.0.{}".format(((rlCount+j)*2)+4, ((rlCount+i+1)*2)+3))
            net['nat{}'.format(i)].cmd("ip route add 10.0.0.{}/31 via 10.0.0.{}".format(((rlCount+j)*2)+4, ((rlCount+i+1)*2)+3))

        for j in range(1, rlCount+i+1):
            print('nat{}'.format(i), "ip route add 10.0.0.{}/31 via 10.0.0.{}".format(j*2, ((rlCount+i+1)*2)))
            net['nat{}'.format(i)].cmd("ip route add 10.0.0.{}/31 via 10.0.0.{}".format(j*2, ((rlCount+i+1)*2)))

    for i in range(1, rlCount + natCount+1):
        print("client" ,"ip route add 10.0.0.{}/31 via 10.0.0.3".format(i*2 + 2))
        net['client'].cmd("ip route add 10.0.0.{}/31 via 10.0.0.3".format(i*2 + 2))

    for i in range(1, rlCount + natCount+1):
        print("server", "ip route add 10.0.0.{}/31 via 10.0.0.{}".format(i*2, (rlCount + natCount)*2 + 2))
        net['server'].cmd("ip route add 10.0.0.{}/31 via 10.0.0.{}".format(i*2, (rlCount + natCount)*2 + 2))
    
    for i in range(rlCount):
        for j in range(i+1, rlCount + natCount):
            print('rl{}'.format(i), "ip route add 10.0.0.{}/31 via 10.0.0.{}".format((j*2)+4, ((i+1)*2)+3))
            net['rl{}'.format(i)].cmd("ip route add 10.0.0.{}/31 via 10.0.0.{}".format((j*2)+4, ((i+1)*2)+3))

        for j in range(1, i+1):
            print('rl{}'.format(i), "ip route add 10.0.0.{}/31 via 10.0.0.{}".format(j*2, ((i+1)*2)))
            net['rl{}'.format(i)].cmd("ip route add 10.0.0.{}/31 via 10.0.0.{}".format(j*2, ((i+1)*2)))

    

    rl_ip_mac = []
    for i in range(0, rlCount):
        if i<9:
            rl_ip_mac.append(("rl{}-0".format(i), "rl{}-1".format(i) ,"10.0.0.{}".format(str((i+1)*2+1)),"10.0.0.{}".format(str((i+1)*2+2)), "00:00:00:00:00:0{}".format(i+1), "00:00:00:00:11:0{}".format(i+1)))
        else:
            rl_ip_mac.append(("rl{}-0".format(i), "rl{}-1".format(i), "10.0.0.{}".format(str((i+1)*2+1)),"10.0.0.{}".format(str((i+1)*2+2)), "00:00:00:00:00:{}".format(i+1), "00:00:00:00:11:{}".format(i+1)))

    nat_ip = []

    for i in range(0, natCount):
        if i<9:
            nat_ip.append(("nat{}-0".format(i), "nat{}-1".format(i), "10.0.0.{}".format(str(((rlCount + i)*2 + 3))), "10.0.0.{}".format(str((rlCount + i)*2 + 4))), "00:00:00:22:00:0{}".format(i+1), "00:00:00:22:11:0{}".format(i+1))
        else:
            nat_ip.append(("nat{}-0".format(i), "nat{}-1".format(i), "10.0.0.{}".format(str(((rlCount + i)*2 + 3))), "10.0.0.{}".format(str((rlCount + i)*2 + 4))), "00:00:00:22:00:{}".format(i+1), "00:00:00:22:11:{}".format(i+1))


    for i, (intf1, intf2, ip1, ip2, mac1, mac2) in enumerate(rl_ip_mac):
        net["rl{}".format(i)].cmdPrint('./venv/bin/python rl.py --clientIp "{}" --clientIface "{}" --serverIp "{}" --serverIface "{}" --agentIp "{}" --agentPort {} --mac1 "{}" --mac2 "{}" &'.format(ip1, intf1, ip2, intf2, AGENT_IP, AGENT_PORT, mac1, mac2))
        time.sleep(1)
    net["server"].cmdPrint('./venv/bin/python server.py -c ./ssl/ssl_cert.pem -k ./ssl/ssl_key.pem --port 1000 -v &')
    time.sleep(1)
    net["client"].cmdPrint('./venv/bin/python client.py --host {} --port 1000 -v'.format("10.0.0.{}".format((rlCount + natCount)*2 + 3)))
   
    CLI(net)
   


    # for i in range(0, rlCount):
    #     if i < 9:
    #         net['rl{}'.format(i)].setMAC('00:00:00:00:00:0{}'.format(i+1), intf='rl{}-0'.format(i))
    #         net['rl{}'.format(i)].setMAC('00:00:00:00:11:0{}'.format(i+1), intf='rl{}-1'.format(i))
    #     else:
    #         net['rl{}'.format(i)].setMAC('00:00:00:00:00:{}'.format(i+1), intf='rl{}-0'.format(i))
    #         net['rl{}'.format(i)].setMAC('00:00:00:00:11:{}'.format(i+1), intf='rl{}-1'.format(i))

    # # list of ip and mac tuples of RL
    # rl_ip_mac = []
    # for i in range(0, rlCount):
    #     if i<9:
    #         rl_ip_mac.append(("rl{}-0".format(i), "rl{}-1".format(i) ,"10.0.0.{}".format(str((i+1)*2+1)),"10.0.0.{}".format(str((i+1)*2+2)), "00:00:00:00:00:0{}".format(i+1), "00:00:00:00:11:0{}".format(i+1)))
    #     else:
    #         rl_ip_mac.append(("rl{}-0".format(i), "rl{}-1".format(i), "10.0.0.{}".format(str((i+1)*2+1)),"10.0.0.{}".format(str((i+1)*2+2)), "00:00:00:00:00:{}".format(i+1), "00:00:00:00:11:{}".format(i+1)))

    # nat_ip = []
    # print(rl_ip_mac)

    # for i in range(0, natCount):
    #     nat_ip.append(("nat{}-0".format(i), "nat{}-1".format(i), "10.0.0.{}".format(str(((rlCount + i)*2 + 3))), "10.0.0.{}".format(str((rlCount + i)*2 + 4))))

    # print(nat_ip)

    # CLI(net)
    net.stop()

# ./venv/bin/python rl.py --clientIp "10.0.0.3" --clientIface "rl0-0" --serverIp "10.0.0.4" --serverIface "rl0-1" --agentIp "10.0.0.22" --agentPort 12001 --mac1 "00:00:00:00:00:01" --mac2 "00:00:00:00:11:01" 
if __name__ == '__main__':
    setLogLevel('info')
    run()