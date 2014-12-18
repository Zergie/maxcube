# -*- coding: utf-8 -*-

from pprint import pprint

def display(s):
	try:
		display(s.__dict__)
	except:
		pprint(s)