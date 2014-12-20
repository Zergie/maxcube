#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import base64
from scapy.all import *

try:
	from maxcube import parsing
except ImportError:
	import os.path
	sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir))
	
	from maxcube import parsing
from maxcube import output


def pkt_callback(pkt):
	global f

	if pkt[IP].src == CUBE_IP:
		print ('<- incoming')
	else:
		print ('-> outgoing')

	try:
		load = pkt.load
		print "load: " + repr(pkt.load)
	except:
		load = ''
		print "str:  " + repr(str(pkt[TCP]))


	r_comment = ''
	r_hex     = ''
	r_bin     = ''

	if load.startswith('s:'):
		r_hex = repr([hex(ord(i)) for i in base64.decodestring(load[2:-2])])
		r_bin = repr([bin(ord(i)) for i in base64.decodestring(load[2:-2])])
		print r_hex
		r_comment = raw_input("comment:")

	if len(r_comment) > 0:
		msg = ('#' * 10         + '\n') + \
			  ('# ' + r_comment + '\n') + \
			  (r_hex            + '\n') + \
			  (r_bin            + '\n\n\n')
		f.write(msg)

	#print pkt.command()


def pkt_filter(pkt):
	if IP in pkt:
		return (pkt[IP].src == CUBE_IP) or (pkt[IP].dst == CUBE_IP)
	else:
		return False


def main():
	global CUBE_IP
	global f

	CUBE_IP = sys.argv[1]

	f = open('log.txt', 'a')
	f.write(repr('== new session ==\n'))

	try:
		sniff(prn=pkt_callback, lfilter=pkt_filter, store=0)
	except KeyboardInterrupt:
		f.close()

if __name__ == '__main__':
	main()