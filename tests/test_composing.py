# -*- coding: utf-8 -*-
from nose import tools

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'maxcube'))

import datetime

from maxcube.client_commands import *
from maxcube.cube_commands import *

def test_simple():
	composed = l_Message().compose()
	tools.assert_equal(composed, b'l:\r\n')

	composed = q_Message().compose()
	tools.assert_equal(composed, b'q:\r\n')


def test_c_Message():
	values   = {'rf_address' : '0fc380'}
	composed = c_Message().compose(values)
	tools.assert_equal(composed, b'c:0fc380\r\n')


#def test_s_Message():
	# values   = {'rf_address' : b'0fc380',
	# 			'room_id'    : 0,
	# 			'temp'       : OFF,
	# 			'temp_mode'  : auto,
	# 			'type'       : 0x22,
	# 			'unknown2'   : 0x00
	# 			}
	# composed = s_Message().compose(values)
	# tools.assert_equal(composed, b's:AAAiAAAAD8OAAAE=\r\n')

	# values   = {'rf_address' : b'0fc380',
	# 			'room_id'    : 0,
	# 			'temp'       : 21.5,
	# 			'temp_mode'  : auto,
	# 			'type'       : 0x11,
	# 			'unknown2'   : 0x00,
	# 			'unknown11'  : b'213d09071803'
	# 			}
	# composed = s_Message().compose(values)
	# tools.assert_equal(composed, b's:AAARAAAAD8OAACshPQkHGAM=\r\n')

	# values   = {'rf_address' : b'0fc373',
	# 			'room_id'    : 0,
	# 			'temp'       : 7.5,
	# 			'temp_mode'  : auto,
	# 			'type'       : 0x20,
	# 			'unknown2'   : 0x00
	# 			}
	# composed = s_Message().compose(values)
	# tools.assert_equal(composed, b's:AAAgAAAAD8NzAA/a7QE=\r\n')

	# values   = {'rf_address' : b'0fc380',
	# 			'room_id'    : 1,
	# 			'temp'       : 1,
	# 			'temp_mode'  : auto,
	# 			'type'       : 0x10,
	# 			'unknown2'   : 0x04,
	# 			'unknown10'  : b'40494c6e40cb4d204d204d204d20'
	# 			}
	# composed = s_Message().compose(values)
	# tools.assert_equal(composed, b's:AAQQAAAAD8OAAQJASUxuQMtNIE0gTSBNIA==\r\n')



def test_H_Message():
	values   = {'rf_address'         : '03f6c9',
				'serial'             : 'JEQ0543545',
				'unknown'            : '00000000',
				'unknown2'           : '0000',
				'clock_set'          : '03',
				'duty_cycle'         : '00',
				'firmware_version'   : '0113',
				'free_memory_slots'  : '32',
				'http_connection_id' : '4f001e1b',
				'cube_date'          : datetime.date(2013, 12, 29),
				'cube_time'          : datetime.time(16, 19)
				}
	composed = H_Message().compose(values)
	tools.assert_equal(composed, b'H:JEQ0543545,03f6c9,0113,00000000,4f001e1b,00,32,0d0c1d,1013,03,0000\r\n')


def test_M_Message():
	values   = {'rooms'           : [{'id'         : 2,
									  'name'       : 'Obyvaci pokoj',
									  'rf_address' : b'08b6d2'},
									 {'id'         : 1,
									  'name'       : 'Predsin',
									  'rf_address' : b'0b04be'}],
				'devices'         : [{'type'       : 2,
				 					  'rf_address' : b'0b04be',
				 					  'serial'     : 'KEQ0571674',
				 					  'name'       : 'topeni u wc',
				 					  'room_id'    : 1},
				 					 {'type'       : 2,
				 					  'rf_address' : b'08b6d2',
				 					  'serial'     : 'KEQ0634607',
				 					  'name'       : 'Pod oknem',
				 					  'room_id'    : 2},
				 					 {'type'       : 5,
				 					  'rf_address' : b'01b491',
				 					  'serial'     : 'JEQ0305205',
				 					  'name'       : 'Eco Switch',
				 					  'room_id'    : 0}],
				'unknown3'        : 1}
	composed = M_Message().compose(values)
	tools.assert_equal(composed, b'M:00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\n')


