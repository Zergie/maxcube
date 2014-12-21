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
#    parsed = start(b'C:03f6c9,7QP2yQATAf9KRVEwNTQzNTQ1AQsABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsABEAAAAAAAAAAQQAAAAAAAAAAAAAAAAAAAAAAAAAAAGh0dHA6Ly93d3cubWF4LXBvcnRhbC5lbHYuZGU6ODAvY3ViZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAENFVAAACgADAAAOEENFU1QAAwACAAAcIA==\r\n')
#    tools.assert_equal(237,              parsed[0].data_len)  
#    tools.assert_equal(b'03f6c9',        parsed[0].rf_address)        
#    tools.assert_equal('JEQ0543545',     parsed[0].serial)            
#    tools.assert_equal(0,                parsed[0].type)
#    tools.assert_equal(1,                parsed[0].firmware_version)
#    tools.assert_equal(19,               parsed[0].room_id) 
#    tools.assert_equal(255,              parsed[0].test_result)
#    tools.assert_equal('http://www.max-portal.elv.de:80/cube',
#                                         parsed[0].portal_url)
#
#    parsed = start(b'C:01b491,EQG0kQUAEg9KRVEwMzA1MjA1\r\n')
#    tools.assert_equal(17,             parsed[0].data_len)
#    tools.assert_equal(b'01b491',      parsed[0].rf_address)
#    tools.assert_equal('JEQ0305205',   parsed[0].serial)
#    tools.assert_equal(5,              parsed[0].type)
#    tools.assert_equal(18,             parsed[0].firmware_version)
#    tools.assert_equal(0,              parsed[0].room_id)
#    tools.assert_equal(15,             parsed[0].test_result)

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
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_mon)
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_tue)
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_wed)
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_thu)
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_fri)
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_sat)
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], 
#                                       parsed[0].program_sun)

    parsed = start(b'C:08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\n')
    

#def test_parsing_output_C():
#    tools.assert_equal(
#        {
#            'data_len': 237,
#            'rf_address': b'03f6c9',
#            'serial': b'JEQ0543545',
#            'type': 0,
#            'fw_version': 1,
#            'room_id': 19,
#            'test_result': 255
#        },
#        handle_output_C(
#            b'03f6c9,7QP2yQATAf9KRVEwNTQzNTQ1AQsABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsABEAAAAAAAAAAQQAAAAAAAAAAAAAAAAAAAAAAAAAAAGh0dHA6Ly93d3cubWF4LXBvcnRhbC5lbHYuZGU6ODAvY3ViZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAENFVAAACgADAAAOEENFU1QAAwACAAAcIA==\r\n'
#        )
#    )
#
    #
#    ref = handle_output_C(b'0b04be,0gsEvgIBEP9LRVEwNTcxNjc0LCE9CQcYA1CH/wBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIA==')
#
#    tools.assert_equal(b'0b04be',      ref['rf_address'])
#    tools.assert_equal(80,             ref['duration_boost'])
#    tools.assert_equal(0.0,            ref['temperature_offset'])
#    tools.assert_equal(255,            ref['test_result'])
#    tools.assert_equal(2,              ref['type'])
#    tools.assert_equal(b'\x87',        ref['decalcification'])
#    tools.assert_equal(b'KEQ0571674',  ref['serial'])
#    tools.assert_equal(16.5,           ref['temperature_eco'])
#    tools.assert_equal(1,              ref['room_id'])
#    tools.assert_equal(210,            ref['data_len'])
#    tools.assert_equal(0.0,            ref['valve_offset'])
#    tools.assert_equal(3,              ref['duration_window_open'])
#    tools.assert_equal(30.5,           ref['temperature_setpoint_max'])
#    tools.assert_equal(100.0,          ref['valve_maximum'])
#    tools.assert_equal(4.5,            ref['temperature_setpoint_min'])
#    tools.assert_equal(16,             ref['fw_version'])
#    tools.assert_equal(22.0,           ref['temperature_comfort'])
#    tools.assert_equal(12.0,           ref['temperature_window_open'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_mon'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_tue'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_wed'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_thu'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_fri'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_sat'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_sun'])
#
#
#    ref = handle_output_C(b'08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA==')
#
#    tools.assert_equal(80,             ref['duration_boost'])
#    tools.assert_equal(2,              ref['room_id'])
#    tools.assert_equal(0,              ref['test_result'])
#    tools.assert_equal(0.0,            ref['valve_offset'])
#    tools.assert_equal(30.5,           ref['temperature_setpoint_max'])
#    tools.assert_equal(100.0,          ref['valve_maximum'])
#    tools.assert_equal(4.5,            ref['temperature_setpoint_min'])
#    tools.assert_equal(210,            ref['data_len'])
#    tools.assert_equal(0.0,            ref['temperature_offset'])
#    tools.assert_equal(16.5,           ref['temperature_eco'])
#    tools.assert_equal(12.0,           ref['temperature_window_open'])
#    tools.assert_equal(23.0,           ref['temperature_comfort'])
#    tools.assert_equal(16,             ref['fw_version'])
#    tools.assert_equal(2,              ref['type'])
#    tools.assert_equal(b'08b6d2',      ref['rf_address'])
#    tools.assert_equal(3,              ref['duration_window_open'])
#    tools.assert_equal(b'\x0c',        ref['decalcification'])
#    tools.assert_equal(b'KEQ0634607',  ref['serial'])
#    print(ref['program_sat'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_sat'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_sun'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_mon'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_tue'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_wed'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_thu'])
#    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_fri'])
#
#
#    ref = handle_output_C(b'C:01b491,EQG0kQUAEg9KRVEwMzA1MjA1')
#
#    tools.assert_equal(17,             ref['data_len'])
#    tools.assert_equal(b'01b491',      ref['rf_address'])
#    tools.assert_equal(b'JEQ0305205',  ref['serial'])
#    tools.assert_equal(5,              ref['type'])
#    tools.assert_equal(18,             ref['fw_version'])
#    tools.assert_equal(0,              ref['room_id'])
#    tools.assert_equal(15,             ref['test_result'])
#
#
#def test_parsing_output_L():
#    tools.assert_equal(
#        {
#            b'01b491': {
#                '?1': 92,
#                'flags_1': 18,
#                'flags_2': 16,
#                'len': 6,
#                'rf_address': b'01b491',
#            },
#            b'08b6d2': {
#                '?1': 92,
#                'date_until': b'\x00\xe1',
#                'flags_1': 18,
#                'flags_2': 24,
#                'len': 11,
#                'rf_address': b'08b6d2',
#                'temperature_setpoint': 17.0,
#                'time_until': b'\x00',
#                'valve_position': 0,
#            },
#            b'0b04be': {
#                '?1': 246,
#                'date_until': b'\x00\xdb',
#                'flags_1': 18,
#                'flags_2': 24,
#                'len': 11,
#                'rf_address': b'0b04be',
#                'temperature_setpoint': 17.0,
#                'time_until': b'\x00',
#                'valve_position': 0,
#            },
#        },
#        handle_output_L(
#            b'CwsEvvYSGAAiANsACwi20lwSGAAiAOEABgG0kVwSEF=='
#        )
#    )

if __name__ == '__main__':
    test_c_message()