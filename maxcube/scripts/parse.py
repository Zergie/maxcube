#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from pprint import pprint

try:
	from maxcube import parsing
except ImportError:
	import os.path
	sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir))
	
	from maxcube import parsing
from maxcube import output


def main():

	print('parsing ', repr(sys.argv[1]))
	message = parsing.start(bytes(sys.argv[1], "utf-8"))
	output.display(message[0])

	if message[0] == None:
		f = open('log.txt', 'a')
	#	f.write(repr(sys.argv[1]) + '\n')
		f.close()
	elif message[0].msg_type == b's:' or message[0].msg_type == b'S:' :
		f = open('log.txt', 'a')
		#f.write(message[0].__dict__ + '\n')
		pprint(message[0].__dict__, f)
		f.close()



if __name__ == '__main__':
	main()