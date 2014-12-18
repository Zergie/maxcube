#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

try:
	from maxcube import parsing
except ImportError:
	import os.path
	sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir))
	
	from maxcube import parsing


from maxcube import output
from maxcube import network
from maxcube import objects

def main():
    raw_data = network.read_raw_data(sys.argv[1], int(sys.argv[2]))
    cube = objects.from_parsed_data(parsing.start(raw_data))
    output.display(cube)


if __name__ == '__main__':
    main()
