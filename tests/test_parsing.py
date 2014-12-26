# -*- coding: utf-8 -*-
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from nose import tools
from maxcube.parsing import start
from pprint import pprint

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

def test_h_message():
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

def test_m_message():
    parsed = start(b'M:00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\n')
    tools.assert_equal(b'M:',        parsed[0].msg_type)
    tools.assert_equal('00',         parsed[0].unknown)
    tools.assert_equal('01',         parsed[0].unknown2)
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

def test_c_message():
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
    tools.assert_equal(30.5,           parsed[0].temperature_setpoint_max)
    tools.assert_equal(4.5,            parsed[0].temperature_setpoint_min)
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
    tools.assert_equal(30.5,           parsed[0].temperature_setpoint_max)
    tools.assert_equal(100.0,          parsed[0].valve_maximum)
    tools.assert_equal(4.5,            parsed[0].temperature_setpoint_min)
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

def test_l_message():
    parsed = start(b'L:CwsEvvYSGAAiANwACwi20lwSGAAiAOcABgG0kVwSEF==\r\n')

    tools.assert_equal(len(parsed)           , 1)
    tools.assert_equal(len(parsed[0].devices), 3)

    pprint(parsed[0].devices[0].__dict__)

    tools.assert_equal(246         , parsed[0].devices[0].unknown)
    tools.assert_equal(None        , parsed[0].devices[0].date_until)
    tools.assert_equal(18          , parsed[0].devices[0].flags_1)
    tools.assert_equal(24          , parsed[0].devices[0].flags_2)
    tools.assert_equal(11          , parsed[0].devices[0].length)
    tools.assert_equal(b'0b04be'   , parsed[0].devices[0].rf_address)
    tools.assert_equal(17.0        , parsed[0].devices[0].temperature_setpoint)
    tools.assert_equal(None        , parsed[0].devices[0].time_until)
    tools.assert_equal(0           , parsed[0].devices[0].valve_position)

    tools.assert_equal(92          , parsed[0].devices[1].unknown)
    tools.assert_equal(None        , parsed[0].devices[1].date_until)
    tools.assert_equal(18          , parsed[0].devices[1].flags_1)
    tools.assert_equal(24          , parsed[0].devices[1].flags_2)
    tools.assert_equal(11          , parsed[0].devices[1].length)
    tools.assert_equal(b'08b6d2'   , parsed[0].devices[1].rf_address)
    tools.assert_equal(17.0        , parsed[0].devices[1].temperature_setpoint)
    tools.assert_equal(None        , parsed[0].devices[1].time_until)
    tools.assert_equal(0           , parsed[0].devices[1].valve_position)

    tools.assert_equal(92          , parsed[0].devices[2].unknown)
    tools.assert_equal(18          , parsed[0].devices[2].flags_1)
    tools.assert_equal(16          , parsed[0].devices[2].flags_2)
    tools.assert_equal(6           , parsed[0].devices[2].length)
    tools.assert_equal(b'01b491'   , parsed[0].devices[2].rf_address)



if __name__ == '__main__':
    test_l_message()
