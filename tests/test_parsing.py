# -*- coding: utf-8 -*-
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from nose import tools
from maxcube.parsing import start
from maxcube.constants import *
from maxcube.output import display

import datetime


RAW_DATA = b'H:JEQ0543545,03f6c9,0113,00000000,4f001e1b,00,32,0d0c1d,1013,03,0000\r\n' + \
		   b'M:00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\n' + \
		   b'C:03f6c9,7QP2yQATAf9KRVEwNTQzNTQ1AQsABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsABEAAAAAAAAAAQQAAAAAAAAAAAAAAAAAAAAAAAAAAAGh0dHA6Ly93d3cubWF4LXBvcnRhbC5lbHYuZGU6ODAvY3ViZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAENFVAAACgADAAAOEENFU1QAAwACAAAcIA==\r\n' + \
		   b'C:0b04be,0gsEvgIBEP9LRVEwNTcxNjc0LCE9CQcYA1AM/wBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\n' + \
		   b'C:08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\n' + \
		   b'C:01b491,EQG0kQUAEg9KRVEwMzA1MjA1\r\n' + \
		   b'L:CwsEvvYSGAAiANwACwi20lwSGAAiAOcABgG0kVwSEF==\r\n'

def test_parser():
	parsed = start(RAW_DATA)
	
	tools.assert_equal(b'H:', parsed[0].msg_type)
	tools.assert_equal(b'M:', parsed[1].msg_type)
	tools.assert_equal(b'C:', parsed[2].msg_type)
	tools.assert_equal(b'C:', parsed[3].msg_type)
	tools.assert_equal(b'C:', parsed[4].msg_type)
	tools.assert_equal(b'C:', parsed[5].msg_type)
	tools.assert_equal(b'L:', parsed[6].msg_type)

	tools.assert_equal(7    , len(parsed))

def test_H_message():
	parsed = start(b'H:JEQ0543545,03f6c9,0113,00000000,4f001e1b,00,32,0d0c1d,1013,03,0000\r\n')
	tools.assert_equal(b'H:' ,       parsed[0].msg_type)
	tools.assert_equal('03f6c9',     parsed[0].rf_address)
	tools.assert_equal('JEQ0543545', parsed[0].serial)
	tools.assert_equal('00000000',   parsed[0].unknown)
	tools.assert_equal('0000',       parsed[0].unknown2)
	tools.assert_equal('03',         parsed[0].clock_set)
	tools.assert_equal('00',         parsed[0].duty_cycle)
	tools.assert_equal('0113',       parsed[0].firmware_version)
	tools.assert_equal('32',         parsed[0].free_memory_slots)
	tools.assert_equal('4f001e1b',   parsed[0].http_connection_id)
	tools.assert_equal(datetime.date(2013, 12, 29), parsed[0].cube_date)
	tools.assert_equal(datetime.time(16, 19),        parsed[0].cube_time)

def test_M_message():
	parsed = start(b'M:00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\n')
	tools.assert_equal(b'M:',        parsed[0].msg_type)
	tools.assert_equal(b'00',        parsed[0].index)
	tools.assert_equal(b'01',        parsed[0].count)
	tools.assert_equal(2,            parsed[0].version)
	tools.assert_equal(86,           parsed[0].magicbyte)
	tools.assert_equal(1,            parsed[0].unknown3)

	tools.assert_equal(3,            len(parsed[0].devices))
	tools.assert_equal(1,                parsed[0].devices[0].room_id)
	tools.assert_equal(b'0b04be',        parsed[0].devices[0].rf_address)
	tools.assert_equal('KEQ0571674',     parsed[0].devices[0].serial)
	tools.assert_equal(2,                parsed[0].devices[0].type)
	tools.assert_equal('topeni u wc',    parsed[0].devices[0].name)
	
	tools.assert_equal(2,                parsed[0].devices[1].room_id)
	tools.assert_equal(b'08b6d2',        parsed[0].devices[1].rf_address)
	tools.assert_equal('KEQ0634607',     parsed[0].devices[1].serial)
	tools.assert_equal(2,                parsed[0].devices[1].type)
	tools.assert_equal('Pod oknem',      parsed[0].devices[1].name)

	tools.assert_equal(0,                parsed[0].devices[2].room_id)
	tools.assert_equal(b'01b491',        parsed[0].devices[2].rf_address)
	tools.assert_equal('JEQ0305205',     parsed[0].devices[2].serial)
	tools.assert_equal(5,                parsed[0].devices[2].type)
	tools.assert_equal('Eco Switch',     parsed[0].devices[2].name)


	tools.assert_equal(2,            len(parsed[0].rooms))
	tools.assert_equal(2,                parsed[0].rooms[0].id)
	tools.assert_equal(b'08b6d2',        parsed[0].rooms[0].rf_address)
	tools.assert_equal('Obyvaci pokoj',  parsed[0].rooms[0].name)

	tools.assert_equal(1,                parsed[0].rooms[1].id)
	tools.assert_equal(b'0b04be',        parsed[0].rooms[1].rf_address)
	tools.assert_equal('Predsin',        parsed[0].rooms[1].name)

	parsed = start(b'M:\r\n')
	tools.assert_equal(b'M:',        parsed[0].msg_type)

def test_C_message():
	parsed = start(b'C:03f6c9,7QP2yQATAf9KRVEwNTQzNTQ1AQsABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsABEAAAAAAAAAAQQAAAAAAAAAAAAAAAAAAAAAAAAAAAGh0dHA6Ly93d3cubWF4LXBvcnRhbC5lbHYuZGU6ODAvY3ViZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAENFVAAACgADAAAOEENFU1QAAwACAAAcIA==\r\n')
	tools.assert_equal(237,              parsed[0].data_len)  
	tools.assert_equal(b'03f6c9',        parsed[0].rf_address)        
	tools.assert_equal('JEQ0543545',     parsed[0].serial)            
	tools.assert_equal(0,                parsed[0].type)
	tools.assert_equal(1,                parsed[0].firmware_version)
	tools.assert_equal(19,               parsed[0].room_id) 
	tools.assert_equal(255,              parsed[0].test_result)
	tools.assert_equal('http://www.max-portal.elv.de:80/cube',
										 parsed[0].portal_url)

	parsed = start(b'C:01b491,EQG0kQUAEg9KRVEwMzA1MjA1\r\n')
	tools.assert_equal(17,             parsed[0].data_len)
	tools.assert_equal(b'01b491',      parsed[0].rf_address)
	tools.assert_equal('JEQ0305205',   parsed[0].serial)
	tools.assert_equal(5,              parsed[0].type)
	tools.assert_equal(18,             parsed[0].firmware_version)
	tools.assert_equal(0,              parsed[0].room_id)
	tools.assert_equal(15,             parsed[0].test_result)

	parsed = start(b'C:0b04be,0gsEvgIBEP9LRVEwNTcxNjc0LCE9CQcYA1AM/wBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\n')
	tools.assert_equal(b'0b04be',      parsed[0].rf_address)
	tools.assert_equal(80,             parsed[0].duration_boost)
	tools.assert_equal(22.0,           parsed[0].temperature_comfort)
	tools.assert_equal(16.5,           parsed[0].temperature_eco)
	tools.assert_equal(ON,             parsed[0].temperature_setpoint_max)
	tools.assert_equal(OFF,            parsed[0].temperature_setpoint_min)
	tools.assert_equal(0.0,            parsed[0].temperature_offset)
	tools.assert_equal(12.0,           parsed[0].temperature_window_open)
	tools.assert_equal(255,            parsed[0].test_result)
	tools.assert_equal(2,              parsed[0].type)
	tools.assert_equal(12,             parsed[0].decalcification)
	tools.assert_equal('KEQ0571674',   parsed[0].serial)
	tools.assert_equal(1,              parsed[0].room_id)
	tools.assert_equal(210,            parsed[0].data_len)
	tools.assert_equal(0.0,            parsed[0].valve_offset)
	tools.assert_equal(3,              parsed[0].duration_window_open)
	tools.assert_equal(100.0,          parsed[0].valve_maximum)
	tools.assert_equal(16,             parsed[0].firmware_version)
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['mon'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['tue'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['wed'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['thu'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['fri'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['sat'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]],     parsed[0].program['sun'])

	parsed = start(b'C:08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\n')
	tools.assert_equal(80,             parsed[0].duration_boost)
	tools.assert_equal(2,              parsed[0].room_id)
	tools.assert_equal(0,              parsed[0].test_result)
	tools.assert_equal(0.0,            parsed[0].valve_offset)
	tools.assert_equal(ON,             parsed[0].temperature_setpoint_max)
	tools.assert_equal(100.0,          parsed[0].valve_maximum)
	tools.assert_equal(OFF,            parsed[0].temperature_setpoint_min)
	tools.assert_equal(210,            parsed[0].data_len)
	tools.assert_equal(0.0,            parsed[0].temperature_offset)
	tools.assert_equal(16.5,           parsed[0].temperature_eco)
	tools.assert_equal(12.0,           parsed[0].temperature_window_open)
	tools.assert_equal(23.0,           parsed[0].temperature_comfort)
	tools.assert_equal(16,             parsed[0].firmware_version)
	tools.assert_equal(2,              parsed[0].type)
	tools.assert_equal(b'08b6d2',      parsed[0].rf_address)
	tools.assert_equal(3,              parsed[0].duration_window_open)
	tools.assert_equal(12,             parsed[0].decalcification)
	tools.assert_equal('KEQ0634607',   parsed[0].serial)
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['sat'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['sun'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['mon'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['tue'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['wed'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['thu'])
	tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   parsed[0].program['fri'])

def test_L_message():
	parsed = start(b'L:CwsEvvYSGAAiANwACwi20lwSGAAiAOcABgG0kVwSEF==\r\n')

	tools.assert_equal(len(parsed)           , 1)
	tools.assert_equal(len(parsed[0].devices), 3)

	tools.assert_equal(246         , parsed[0].devices[0].unknown)
	tools.assert_equal(None        , parsed[0].devices[0].date_until)
	tools.assert_equal(11          , parsed[0].devices[0].length)
	tools.assert_equal(b'0b04be'   , parsed[0].devices[0].rf_address)
	tools.assert_equal(17.0        , parsed[0].devices[0].temperature_setpoint)
	tools.assert_equal(None        , parsed[0].devices[0].time_until)
	tools.assert_equal(0           , parsed[0].devices[0].valve_position)

	tools.assert_equal(92          , parsed[0].devices[1].unknown)
	tools.assert_equal(None        , parsed[0].devices[1].date_until)
	tools.assert_equal(11          , parsed[0].devices[1].length)
	tools.assert_equal(b'08b6d2'   , parsed[0].devices[1].rf_address)
	tools.assert_equal(17.0        , parsed[0].devices[1].temperature_setpoint)
	tools.assert_equal(None        , parsed[0].devices[1].time_until)
	tools.assert_equal(0           , parsed[0].devices[1].valve_position)

	tools.assert_equal(92          , parsed[0].devices[2].unknown)
	tools.assert_equal(6           , parsed[0].devices[2].length)
	tools.assert_equal(b'01b491'   , parsed[0].devices[2].rf_address)

	parsed = start(b'L:\r\n')
	tools.assert_equal(b'L:',        parsed[0].msg_type)

def test_s_message():
	#  0   , 1   , 2   , 3   , 4   , 5   , 6   , 7   , 8   , 9   , 10
	
	# de.eq3.max.al.core.command.SetRoomPermanentMode
	# |  /  |group| cmd |       /         |    rf adress    |room |temp 
	# |     | cmd?|     |                 |                 |     |     
	# [0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x00, 0x01]

	# de.eq3.max.al.core.command.SetRoomTemporaryMode
	# |  /  |group| cmd |       /         |    rf adress    |room |temp | date      | time
	# |     | cmd?|     |                 |                 |     |     |           |
	# [0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x73, 0x00, 0x0f, 0xda, 0xed, 0x01]

	# de.eq3.max.al.core.command.SetRoomAutoMode
	# |  /  |group| cmd |       /         |    rf adress    |room |temp = 0
	# |     | cmd?|     |                 |                 |     |     
	# [0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x00, 0x00]

	# de.eq3.max.al.core.command.SetRoomAutoModeWithTemperature
	# |  /  |group| cmd |       /         |    rf adress    |room |temp 
	# |     | cmd?|     |                 |                 |     |     
	# [0x00, 0x00, 0x40, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x00, 0x01]

	# cmds
	#0x00		= SystemInformation # not used
	#0x01		= Inclusion # not used
	#0x02		= Answer # not used
	#0x03		= TimeInformation # not used
	#0x10		= ConfigWeekTemperatureProfile
	#0x11		= ConfigTemperatures
	#0x12		= ConfigValveFunctions
	#0x20		= AddLinkPartner
	#0x21		= RemoveLinkPartner
	#0x22		= SetGroupAddress
	#0x23		= RemoveGroupAddress
	#0x30		= ShutterConactState
	#0x40		= ControlMode
	#0x41		= SetPointTemperature
	#0x42		= SetPointAndCurrentTemperature
	#0x43		= ComfortTemperature
	#0x44		= EcoTemperature
	#0x45		= CurrentTemperatureAndHumidity
	#0x50		= PushButtonState
	#0x60		= HeatungThermostatState
	#-0x80		= LockManualControls
	#-0x81		= DaylightSavingTimeMode
	#-0x82		= SwitchDisplaySetPointActual
	#-0xF0		= Reset
	#-0xF1		= WakeUp
	#-0xFF		= Test

	parsed = start(b's:AAAiAAAAD8OAAAE=\r\n')
	# |               magic               |    rf adress    |  /  |room |
	#  0   , 1   , 2   , 3   , 4   , 5   , 6   , 7   , 8   , 9   , 10  , 11  , 12  , 13
	# [0x00, 0x00, 0x22, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x00, 0x01] 
	tools.assert_equal(parsed[0].msg_type   , b's:')
	tools.assert_equal(parsed[0].rf_address , b'0fc380')
	tools.assert_equal(parsed[0].room_id    , 0)
	tools.assert_equal(parsed[0].new_room_id, 1)

	parsed = start(b's:AAARAAAAD8OAACshPQkHGAM=\r\n') 
	# |               magic               |    rf adress    |room |temp|   
	# [0x00, 0x00, 0x11, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x00, 0x2b, 0x21, 0x3d, 0x09, 0x07, 0x18, 0x03]
	tools.assert_equal(parsed[0].msg_type                , b's:')
	tools.assert_equal(parsed[0].rf_address              , b'0fc380')
	tools.assert_equal(parsed[0].room_id                 , 0)
	tools.assert_equal(parsed[0].temperature_comfort     , 21.5)
	tools.assert_equal(parsed[0].temperature_eco         , 16.5)
	tools.assert_equal(parsed[0].temperature_setpoint_max, ON)
	tools.assert_equal(parsed[0].temperature_setpoint_min, OFF)
	tools.assert_equal(parsed[0].temperature_offset      , 0)
	tools.assert_equal(parsed[0].temperature_window_open , 12.0)
	tools.assert_equal(parsed[0].duration_window_open    , 3)
	
	parsed = start(b's:AAAgAAAAD8NzAA/a7QE=\r\n') 
	# |               magic               |    rf adress    |room | rf adress dst   | type dst
	# [0x00, 0x00, 0x20, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x73, 0x00, 0x0f, 0xda, 0xed, 0x01]
	tools.assert_equal(parsed[0].msg_type              , b's:')
	tools.assert_equal(parsed[0].rf_address            , b'0fc373')
	tools.assert_equal(parsed[0].room_id               , 0)
	tools.assert_equal(parsed[0].destination_rf_address, b'0fdaed')
	tools.assert_equal(parsed[0].destination_type      , 1)
	tools.assert_equal(parsed[0].group                 , False)

	parsed = start(b's:AAQQAAAAD8OAAQJASUxuQMtNIE0gTSBNIA==\r\n') 
	# |               magic               |    rf adress    |room | day |temp |time | day2|temp |time | day3|temp |time | day4|temp |time | day5|temp |time |
	#  0   , 1   , 2   , 3   , 4   , 5   , 6   , 7   , 8   , 9   , 10  , 11  , 12  , 13  , 14  , 15  , 16  , 17  , 18  , 19  , 20  , 21  , 22  , 23  , 24
	# [0x00, 0x04, 0x10, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x01, 0x02, 0x40, 0x49, 0x4c, 0x6e, 0x40, 0xcb, 0x4d, 0x20, 0x4d, 0x20, 0x4d, 0x20, 0x4d, 0x20]
	tools.assert_equal(parsed[0].msg_type              , b's:')
	tools.assert_equal(parsed[0].rf_address            , b'0fc380')
	tools.assert_equal(parsed[0].room_id               , 1)
	tools.assert_equal(parsed[0].day                   , 2)
	tools.assert_equal(parsed[0].program[0].temperature, 16)
	tools.assert_equal(parsed[0].program[0].time       , datetime.time(6, 5))
	tools.assert_equal(parsed[0].program[1].temperature, 19)
	tools.assert_equal(parsed[0].program[1].time       , datetime.time(9, 10))
	tools.assert_equal(parsed[0].program[2].temperature, 16)
	tools.assert_equal(parsed[0].program[2].time       , datetime.time(16, 55))
	tools.assert_equal(parsed[0].group                 , True)

	parsed = start(b's:AARAAAAAD8OAAaveDiI=\r\n')
	# |               magic               |    rf adress    |room |temp|   date     |time 
	# [0x00, 0x04, 0x40, 0x00, 0x00, 0x00, 0x0f, 0xc3, 0x80, 0x01, 0xab, 0xde, 0x0e, 0x22]
	tools.assert_equal(parsed[0].msg_type   , b's:')
	tools.assert_equal(parsed[0].rf_address , b'0fc380')
	tools.assert_equal(parsed[0].room_id    , 1)
	tools.assert_equal(parsed[0].temp       , 21.5)
	tools.assert_equal(parsed[0].temp_mode  , vacation)
	tools.assert_equal(parsed[0].date_until , datetime.date(2014, 12, 30))
	tools.assert_equal(parsed[0].time_until , datetime.time(17, 00))

if __name__ == '__main__':
	test_s_message()
