# -*- coding: utf-8 -*-

class Constant(object):
	def __init__(self, text, value=0, representation=None):
		self.text  = text
		self.value = value
		self.repr  = representation

		globals()[text] = self
	def __mul__(self, other):
		return (self.repr * other)
	def __repr__(self):
		return 'CONST ' + self.text


# consts for parsing
Constant('VL')  # variable length (length found in first bit)
Constant('ALL') # no length restriction
Constant('T0')  # decode until 0x00

# temperature values
Constant('ON', 30.5, 30.5)
Constant('OFF', 4.5, 0.5)

# temperature modes
Constant('auto'    , 0b00000000)
Constant('manual'  , 0b01000000)
Constant('vacation', 0b10000000)
Constant('boost'   , 0b11000000)