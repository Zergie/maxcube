# -*- coding: utf-8 -*-

class Constant(object):
	def __init__(self, text):
		self.text = text
		globals()[text] = self
	def __repr__(self):
		return 'CONST ' + self.text


# consts for parsing
Constant('VL')  # variable length (length found in first bit)
Constant('ALL') # no length restriction
Constant('T0')  # decode until 0x00

# temperature values
Constant('ON')
Constant('OFF')

# temperature modes
Constant('auto')
Constant('manual')
Constant('vacation')
Constant('boost')