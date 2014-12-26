#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import base64
from scapy.all import *


PARSING_PROG = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'parse.py')


def pkt_callback(pkt):
	global f

	if pkt[IP].src == CUBE_IP:
		print ('<- incoming')
	else:
		print ('-> outgoing')

	try:
		load = pkt.load
		#print "load: " + repr(pkt.load)
	except:
		load = ''
		#print "str:  " + repr(str(pkt[TCP]))

	if len(load) > 1 and load[1] == ':':
		cmd = 'python3 "%s" "%s"' % (PARSING_PROG, load.encode("utf-8"))
		os.system(cmd)
		


def pkt_filter(pkt):
	if IP in pkt:
		return (pkt[IP].src == CUBE_IP) or (pkt[IP].dst == CUBE_IP)
	else:
		return False


def main():
	global CUBE_IP
	
	CUBE_IP = sys.argv[1]
	sniff(prn=pkt_callback, lfilter=pkt_filter, store=0)

if __name__ == '__main__':
	main()