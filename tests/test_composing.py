# -*- coding: utf-8 -*-
from nose import tools

from maxcube.parsing import *

def test_simple():
	composed = compose(l_Message)
	tools.assert_equal(composed, b'l:\r\n')

	composed = compose(q_Message)
	tools.assert_equal(composed, b'q:\r\n')


def test_c_Message():
	values   = {'rf_address' : '0fc380'}
	composed = compose(c_Message, values)
	tools.assert_equal(composed, b'c:0fc380\r\n')


def test_s_Message():
	values = {'type'               : AddLinkPartner,
			  'msg_type'           : b's:',
			  'rf_address'         : b'0fc373',
			  'room_id'            : 0,
			  'partner_rf_address' : b'0fdaed',
			  'partner_type'       : 1,
			  'group'              : False}
	composed = compose(s_Message, values)
	tools.assert_equal(composed, b's:AAAgAAAAD8NzAA/a7QE=\r\n')

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
	composed = compose(H_Message, values)
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
	composed = compose(M_Message, values)
	tools.assert_equal(composed, b'M:00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\n')