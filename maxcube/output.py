# -*- coding: utf-8 -*-

def display(s):
	try:
		display(s.__dict__)
	except:
		pprint(s)