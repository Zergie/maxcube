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
		print('Cube:')
		cube = objects.MaxCube(tcp_addr, tcp_port)
		cube.connect()
		output.display(cube)

		thermostat = cube.devices[b'0fc380']
		
		while 1:
			print(thermostat.status())
			temp = input('temp for 0fc380: ')

			if len(temp) > 0:
				thermostat.set_temp(int(temp))
			
			

		cube.close()
	
if __name__ == '__main__':
	main()
    