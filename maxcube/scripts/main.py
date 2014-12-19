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
	cube = objects.MaxCube(sys.argv[1], int(sys.argv[2]))
	cube.connect()
    output.display(cube)


if __name__ == '__main__':
    main()
