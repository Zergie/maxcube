# -*- coding: utf-8 -*-

from maxcube import parsing
from maxcube import output
from maxcube import network
from maxcube import objects


def main():	
	print("searching maxcube(s)..")

	for tcp_addr, tcp_port in network.discover_cubes(limit = 1):
		raw_data = network.read_raw_data(tcp_addr, tcp_port)

		print('')
		print('raw_data:')
		output.display(raw_data)
		
		print('')
		print('parsed_data:')
		parsed_data = parsing.start(raw_data)
		output.display(parsed_data)
		
		print('')
		print('Cube:')
		cube = objects.from_parsed_data(parsed_data)
		output.display(cube)
	
if __name__ == '__main__':
	main()
    