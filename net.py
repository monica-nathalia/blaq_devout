#!/usr/bin/env python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import lg, info, setLogLevel
from mininet.cli import CLI
from mininet.node import Switch, OVSKernelSwitch
from mininet.node import OVSController
from mininet.nodelib import LinuxBridge
from argparse import ArgumentParser

import sys
import os
import termcolor as T
import time

setLogLevel('info')

parser = ArgumentParser("Configure simple network in Mininet.")
parser.add_argument('--sleep', default=3, type=int)
args = parser.parse_args()

class myTopo( Topo ):
    "Simple topology example."

    def __init__( self ):
        "Create custom topo."

        # Initialize topology
        Topo.__init__( self )

        self.addHost('h0')
        self.addHost('h1')
        self.addHost('h3')

        self.addSwitch('h2', cls=LinuxBridge)
        self.addLink('h1','h2')
        self.addLink('h3','h2')

        # desktops = [self.addHost( 'h%d'%i ) for i in range(4)]
        # h1 = self.getNodeByName('h1')
        # h2 = self.getNodeByName('h2')
        # h3 = self.getNodeByName('h3')
        # leftSwitch = self.addSwitch( 's1' )
        # rightSwitch = self.addSwitch( 's2' )
        # comswitch = self.addSwitch('s0')

        # Add links
        # let h2 be bridge between h1 & h3
        # so we run packet capturing at h2

        # self.addLink('h3', 'h2', intfName1="h3-h2eth", intfName2="h2-h3eth")
        # h3.intf("h3-h2eth").setIP('10.0.1.2')
        # h2.intf("h2-h3eth").setIP('10.0.1.1')
        # self.addLink('h1', 'h2', intfName1="h1-h2eth", intfName2="h2-h1eth")
        # h1.intf("h1-h2eth").setIP('10.0.0.1')
        # h2.intf("h2-h1eth").setIP('10.0.0.2')

        # for i in range(len(desktops)):
        #     self.addLink( comswitch, 'h%d'%i)
        return

def log(s, col="green"):
    print T.colored(s, col)

def main():
    os.system("rm -f /tmp/R*.log /tmp/R*.pid logs/*")
    os.system("mn -c >/dev/null 2>&1")

    net = Mininet(topo=myTopo(), controller = OVSController, autoSetMacs=True)

    # adding interface & connections
    # h1 = net.hosts[1]
    # h2 = net.hosts[2]
    # h3 = net.hosts[3]

    # net.addLink('h3', 'h2', intfName1="h3-h2eth", intfName2="h2-h3eth")
    # h3.intf("h3-h2eth").setIP('10.0.1.2', 24)
    # h2.intf("h2-h3eth").setIP('10.0.1.1', 24)

    # net.addLink('h1', 'h2', intfName1="h1-h2eth", intfName2="h2-h1eth")
    # h1.intf("h1-h2eth").setIP('10.0.0.1', 24)
    # h2.intf("h2-h1eth").setIP('10.0.0.2', 24)

    # net.build()
    net.start()
        
    log("Configured the routers")

    for i in range(4):
        host = net.getNodeByName('h%d'%i)
        # host.cmd("cd h%d && ./server.sh &"%i)
        log("Machine started: h%d"%i)

    #bridging connection
    host = net.getNodeByName('h2')
    host.cmd("sudo ./start.sh h2-h1eth h2-h3eth")


    CLI(net)
    net.stop()
    os.system("killall -9 dnsmasq")

if __name__ == "__main__":
    main()
