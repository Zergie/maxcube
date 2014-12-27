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


def test_s_Message():
	values   = {'rf_address' : b'0fc380',
				'room_id'    : 2,
				'temp'       : 20.0,
				'temp_mode'  : auto,
				'date_until' : None,
				'time_until' : None
				}
	composed = s_Message().compose(values)
	tools.assert_equal(composed, b's:AARAAAAAD8OAAig=\r\n')

	values   = {'rf_address' : b'0fc380',
				'room_id'    : 2,
				'temp'       : 22.0,
				'temp_mode'  : manual,
				'date_until' : None,
				'time_until' : None
				}
	composed = s_Message().compose(values)
	tools.assert_equal(composed, b's:AARAAAAAD8OAAmw=\r\n')

	values   = {'rf_address' : b'0fc380',
				'room_id'    : 2,
				'temp'       : 23.0,
				'temp_mode'  : vacation,
				'date_until' : datetime.date(2014, 12, 27),
				'time_until' : datetime.time(20, 30)
				}
	composed = s_Message().compose(values)
	tools.assert_equal(composed, b's:AARAAAAAD8OAAq7bDik=\r\n')

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
# b'H:JEQ0543545,03f6c9,0113,00000000,4f001e1b,00,32,\\xdd\\r, ,03,0000\\r\\n'
# b'H:JEQ0543545,03f6c9,0113,00000000,4f001e1b,00,32,0d0c1d,1013,03,0000\\r\\n'

