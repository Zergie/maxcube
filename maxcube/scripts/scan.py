#!/usr/bin/env python3
# -*- coding: utf-8 -*-

try:
	from maxcube import parsing
except ImportError:
	import os.path, sys
	sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir))
	
	from maxcube import parsing

from maxcube import output
from maxcube import network
from maxcube import objects


def main():	
	print("searching maxcube(s)..")

	for tcp_addr, tcp_port in network.discover_cubes(limit = 1):
		print('')
		print('Cube:', tcp_addr, tcp_port)
		
		cube = objects.MaxCube(tcp_addr, tcp_port)
		cube.connect()
		print(cube)			
		cube.close()
	
if __name__ == '__main__':
	main()
    
