# -*- coding: utf-8 -*-

from pprint import pprint
from maxcube.constants import Constant

def fformat(obj):
	if isinstance(obj, list):
		ret = []
		for i in obj:
			ret.append(fformat(i))
	elif isinstance(obj, dict):
		ret = {}
		for key, value in obj.items():
			ret[key] = fformat(value)
	elif isinstance(obj, Constant):
		ret = obj
	else:
		try:
			ret = fformat(obj.__dict__)
		except:
			ret = obj

	return ret

def display(s):
	pprint(fformat(s))