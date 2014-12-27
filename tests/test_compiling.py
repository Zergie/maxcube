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
	compiled = l_Message().compile()
	tools.assert_equal(compiled, {})

	compiled = q_Message().compile()
	tools.assert_equal(compiled, {})


def test_c_Message():
	compiled = c_Message().compile()
	tools.assert_equal(compiled, {'rf_address': None})


def test_s_Message():
	compiled = s_Message().compile()
	tools.assert_equal(compiled, {'rf_address': None,
								  'room_id'   : None,
								  'temp'      : None,
								  'temp_mode' : None,
								  'date_until': None,
								  'time_until': None})


def test_H_Message():
	compiled = H_Message().compile()
	tools.assert_equal(compiled, {'rf_address'         : None,
								  'serial'             : None,
								  'unknown'            : None,
								  'unknown2'           : None,
								  'clock_set'          : None,
								  'duty_cycle'         : None,
								  'firmware_version'   : None,
								  'free_memory_slots'  : None,
								  'http_connection_id' : None,
								  'cube_date'          : None,
								  'cube_time'          : None})


def test_M_Message():
	compiled = M_Message().compile()
	tools.assert_equal(compiled, {'rooms'           : [{'id'         : None,
														'name'       : None,
														'rf_address' : None}],
									'devices'       : [{'type'       : None,
														'rf_address' : None,
														'serial'     : None,
														'name'       : None,
														'room_id'    : None}],
									'unknown3'      : None})
