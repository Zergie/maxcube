# -*- coding: utf-8 -*-

import socket
from maxcube import bcd


def udp_handshake():
	print("Performing UDP handshake")
	HelloMessage =  bytes([0x65, 0x51, 0x33, 0x4d, 0x61, 0x78, 0x2a, 0x00, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x49]);
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	
	sock.bind(('', 23272))
	sock.sendto(HelloMessage, ('224.0.0.1', 23272))

	while True:
		data, addr = sock.recvfrom(1024)
		
		if data[:8] == b'eQ3MaxAp':
			udp_answer = {
				'serial' : data[8:18],
				'unknown' : data[18:21],
				'rf_address' : data[21:24],
				'fw_version' : bcd.to_int(data[24:26])
				}
			break
	sock.close()
	
	print(udp_answer)
	
	if udp_answer['fw_version'] < 109:
		return addr[0], 80
	else:
		return addr[0], 62910