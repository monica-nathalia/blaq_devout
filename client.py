import socket
import hexdump

from scapy.all import *
from scapy.utils import rdpcap

pkts = rdpcap('samples4.pcap')

counter = 0

def expand(x):
	yield x.name
	while x.payload:
		x = x.payload
		yield x.name

for pkt in pkts[:1]:
	np = pkt.payload
	# print(b'\x73\x74\x56\x61\x6c'.decode())
	print(list(expand(pkt)))
	if 'stVal' in str(np.build()):
		print("oh boy mms here")
		print(np)

	try:
		if IP in pkt:
			# print(np)
			np.show()
			np[IP].dst = '10.0.0.3'
			np[IP].src = '10.0.0.2'
			del np[IP].chksum
			np.show2()
			send(np)
			counter += 1
			print ('packet no: %d' %counter)
		elif pkt.type == 0x88b8:
			#no IP layer found
			#assume goose
			print('assume Goose')
			print(pkt)
			pkt[Ether].src = '00:00:00:00:00:02'
			pkt[Ether].src = '00:00:00:00:00:03'
			sendp(pkt)
			counter += 1
			print ('packet no: %d' %counter)
	except:
		pass

# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # connect the client
# # client.connect((target, port))
# client.connect(('10.0.0.3', 9999))
# # client.bind((" ",1234))

# # send some data (in this case a HTTP GET request)
# msg = hexdump.dehex(
# 	# '00 30 de 40 d0 e2 00 09 8e f8 c4 fe 08 00 45 00\
# 	'03 00 00 22 02 f0 80 01 00 01\
# 00 61 15 30 13 02 01 03 a0 0e a1 0c 02 03 01 fb\
# 4f a4 05 a1 03 83 01 01')
# client.send(msg)

# # receive the response data (4096 is recommended buffer size)
# response = client.recv(4096)

# print(response)