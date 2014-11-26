# -*- coding: utf-8 -*-

def to_int(z):
	result = 0

	for x_byte in z:
		result *= 100
		x = int(x_byte)
		
		a = (x & 0xF0) >> 4
		b = x & 0x0F
		result += (a*10) + b
		
	return result