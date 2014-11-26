# -*- coding: utf-8 -*-

import datetime

from maxcube import objects


IDENT_CHAR = ' '
IDENT_STEP = 2

def display(s):
	print(d(s))


def d(s, ident=0):
	if isinstance(s, dict):
		r = d_dict(s, ident)
	elif isinstance(s, list):
		r = d_list(s, ident)	
	elif isinstance(s, (str, int, bytes, float, datetime.date, datetime.time)):
		r = d_simple(s, ident)
	elif isinstance(s, object):
		r = d_object(s, ident)	
	else:
	    r = repr(s)
	return r




def d_simple(s, ident=0):
	return repr(s)

def d_object(object, ident=0):
	r = repr(object) + '\n' 
	r += IDENT_CHAR*ident + d_dict(object.__dict__, ident)
	return r
	
def d_dict(dict, ident=0):
	keys = sorted(dict.keys())
	
	r = '{\n'
	ident += IDENT_STEP
	
	for k in keys:
		r_key = IDENT_CHAR*ident + repr(k) + ' : '
		r_value = d(dict[k], len(r_key)-IDENT_STEP) + ',\n'
		r += r_key + r_value
		
		
	ident -= IDENT_STEP
	r = r[:-2] + " }"
	return r



def d_list(list, ident):
	r = '[\n'
	ident += IDENT_STEP
	
	for i in list:
		r += IDENT_CHAR*ident + d(i, ident) + ',\n'
		
	ident -= IDENT_STEP
	r = r[:-2] + " ]"
	return r