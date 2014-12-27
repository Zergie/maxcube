# -*- coding: utf-8 -*-
from nose import tools

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'maxcube'))

import datetime

from maxcube.client_commands import *

def test_simple():
	compiled = l_Message().compile()
	tools.assert_equal(compiled, {})

	compiled = q_Message().compile()
	tools.assert_equal(compiled, {})


def test_c_message():
	compiled = c_Message().compile()
	tools.assert_equal(compiled, {'rf_address': None})


def test_s_message():
	compiled = s_Message().compile()
	tools.assert_equal(compiled, {'rf_address': None,
								  'room_id'   : None,
								  'temp'      : None,
								  'temp_mode' : None,
								  'date_until': None,
								  'time_until': None})	
