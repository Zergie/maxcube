# -*- coding: utf-8 -*-
from nose import tools

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'maxcube'))

import datetime

from maxcube.client_commands import *


def test_simple():
	composed = l_Message().compose()
	tools.assert_equal(composed, b'l:\r\n')

	composed = q_Message().compose()
	tools.assert_equal(composed, b'q:\r\n')


def test_c_message():
	values   = {'rf_address' : '0fc380'}
	composed = c_Message().compose(values)
	tools.assert_equal(composed, b'c:0fc380\r\n')


def test_s_message():
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
	