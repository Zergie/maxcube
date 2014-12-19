# -*- coding: utf-8 -*-
import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))

from nose import tools
from maxcube.parsing import handle_output_H, handle_output_M, handle_output_C, handle_output_L, start

import datetime


RAW_DATA = b'H:JEQ0543545,03f6c9,0113,00000000,4f001e1b,00,32,0d0c12,001f,03,0000\r\nM:00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\nC:03f6c9,7QP2yQATAf9KRVEwNTQzNTQ1AQsABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsABEAAAAAAAAAAQQAAAAAAAAAAAAAAAAAAAAAAAAAAAGh0dHA6Ly93d3cubWF4LXBvcnRhbC5lbHYuZGU6ODAvY3ViZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAENFVAAACgADAAAOEENFU1QAAwACAAAcIA==\r\nC:0b04be,0gsEvgIBEP9LRVEwNTcxNjc0LCE9CQcYA1AM/wBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\nC:08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA==\r\nC:01b491,EQG0kQUAEg9KRVEwMzA1MjA1\r\nL:CwsEvvYSGAAiANwACwi20lwSGAAiAOcABgG0kVwSEF==\r\n'

def test_parser():
    parsed = start(RAW_DATA)
    tools.assert_equal(
        {'H', 'C', 'M', 'L'},
        set(parsed.keys())
    )


def test_parsing_output_H():
    tools.assert_equal(
        {
            'firmware_version': '0113',
            'rf_address': '03f6c9',
            'serial': 'JEQ0543545',
            '?1': '00000000',
            '?2': '0000',
            'clock_set': '03',
            'cube_date': datetime.date(2013, 12, 15),
            'cube_time': datetime.time(0, 12),
            'duty_cycle': '00',
            'firmware_version': '0113',
            'free_memory_slots': '32',
            'http_connection_id': '2663651e',
        },
        handle_output_H(
            b'JEQ0543545,03f6c9,0113,00000000,2663651e,00,32,0d0c0f,000c,03,0000\r\n',
        )
    )

def test_parsing_output_M():
    tools.assert_equal(
        {
            'version': 2,
            'room_count': 2,
            'magicbyte': 86,
            'devices': [
                {
                    'room_id': 1,
                    'rf_address': b'0b04be',
                    'serial': b'KEQ0571674',
                    'type': 2,
                    'name_len': 11,
                    'name': b'topeni u wc'
                }, 
                {
                    'room_id': 2,
                    'rf_address': b'08b6d2',
                    'serial': b'KEQ0634607',
                    'type': 2,
                    'name_len': 9,
                    'name': b'Pod oknem'
                }, 
                {
                    'room_id': 0,
                    'rf_address': b'01b491',
                    'serial': b'JEQ0305205',
                    'type': 5,
                    'name_len': 10,
                    'name': b'Eco Switch'
                }],
            '?2': b'\x01',
            'rooms': {
                1: {
                    'id': 1,
                    'rf_address': b'0b04be',
                    'name_len': 7,
                    'name': b'Predsin'
                    },
                2: {
                    'id': 2,
                    'rf_address': b'08b6d2',
                    'name_len': 13,
                    'name': b'Obyvaci pokoj'}
                    },
                'devices_count': 3},
        handle_output_M(
            b'00,01,VgICAg1PYnl2YWNpIHBva29qCLbSAQdQcmVkc2luCwS+AwILBL5LRVEwNTcxNjc0C3RvcGVuaSB1IHdjAQIIttJLRVEwNjM0NjA3CVBvZCBva25lbQIFAbSRSkVRMDMwNTIwNQpFY28gU3dpdGNoAAE=\r\n'
        )
    )

def test_parsing_output_C():
    tools.assert_equal(
        {
            'data_len': 237,
            'rf_address': b'03f6c9',
            'serial': b'JEQ0543545',
            'type': 0,
            'fw_version': 1,
            'room_id': 19,
            'test_result': 255
        },
        handle_output_C(
            b'03f6c9,7QP2yQATAf9KRVEwNTQzNTQ1AQsABEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAsABEAAAAAAAAAAQQAAAAAAAAAAAAAAAAAAAAAAAAAAAGh0dHA6Ly93d3cubWF4LXBvcnRhbC5lbHYuZGU6ODAvY3ViZQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAENFVAAACgADAAAOEENFU1QAAwACAAAcIA==\r\n'
        )
    )

    
    ref = handle_output_C(b'0b04be,0gsEvgIBEP9LRVEwNTcxNjc0LCE9CQcYA1CH/wBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIA==')

    tools.assert_equal(b'0b04be',      ref['rf_address'])
    tools.assert_equal(80,             ref['duration_boost'])
    tools.assert_equal(0.0,            ref['temperature_offset'])
    tools.assert_equal(255,            ref['test_result'])
    tools.assert_equal(2,              ref['type'])
    tools.assert_equal(b'\x87',        ref['decalcification'])
    tools.assert_equal(b'KEQ0571674',  ref['serial'])
    tools.assert_equal(16.5,           ref['temperature_eco'])
    tools.assert_equal(1,              ref['room_id'])
    tools.assert_equal(210,            ref['data_len'])
    tools.assert_equal(0.0,            ref['valve_offset'])
    tools.assert_equal(3,              ref['duration_window_open'])
    tools.assert_equal(30.5,           ref['temperature_setpoint_max'])
    tools.assert_equal(100.0,          ref['valve_maximum'])
    tools.assert_equal(4.5,            ref['temperature_setpoint_min'])
    tools.assert_equal(16,             ref['fw_version'])
    tools.assert_equal(22.0,           ref['temperature_comfort'])
    tools.assert_equal(12.0,           ref['temperature_window_open'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_mon'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_tue'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_wed'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_thu'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_fri'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_sat'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(21, 0)], [21, datetime.time(23, 0)]], ref['program_sun'])


    ref = handle_output_C(b'08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA==')

    tools.assert_equal(80,             ref['duration_boost'])
    tools.assert_equal(2,              ref['room_id'])
    tools.assert_equal(0,              ref['test_result'])
    tools.assert_equal(0.0,            ref['valve_offset'])
    tools.assert_equal(30.5,           ref['temperature_setpoint_max'])
    tools.assert_equal(100.0,          ref['valve_maximum'])
    tools.assert_equal(4.5,            ref['temperature_setpoint_min'])
    tools.assert_equal(210,            ref['data_len'])
    tools.assert_equal(0.0,            ref['temperature_offset'])
    tools.assert_equal(16.5,           ref['temperature_eco'])
    tools.assert_equal(12.0,           ref['temperature_window_open'])
    tools.assert_equal(23.0,           ref['temperature_comfort'])
    tools.assert_equal(16,             ref['fw_version'])
    tools.assert_equal(2,              ref['type'])
    tools.assert_equal(b'08b6d2',      ref['rf_address'])
    tools.assert_equal(3,              ref['duration_window_open'])
    tools.assert_equal(b'\x0c',        ref['decalcification'])
    tools.assert_equal(b'KEQ0634607',  ref['serial'])
    print(ref['program_sat'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_sat'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_sun'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_mon'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_tue'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_wed'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_thu'])
    tools.assert_equal([[23, datetime.time(8, 30)], [22, datetime.time(22, 0)], [21, datetime.time(23, 0)]],   ref['program_fri'])


    ref = handle_output_C(b'C:01b491,EQG0kQUAEg9KRVEwMzA1MjA1')

    tools.assert_equal(17,             ref['data_len'])
    tools.assert_equal(b'01b491',      ref['rf_address'])
    tools.assert_equal(b'JEQ0305205',  ref['serial'])
    tools.assert_equal(5,              ref['type'])
    tools.assert_equal(18,             ref['fw_version'])
    tools.assert_equal(0,              ref['room_id'])
    tools.assert_equal(15,             ref['test_result'])


def test_parsing_output_L():
    tools.assert_equal(
        {
            b'01b491': {
                '?1': 92,
                'flags_1': 18,
                'flags_2': 16,
                'len': 6,
                'rf_address': b'01b491',
            },
            b'08b6d2': {
                '?1': 92,
                'date_until': b'\x00\xe1',
                'flags_1': 18,
                'flags_2': 24,
                'len': 11,
                'rf_address': b'08b6d2',
                'temperature_setpoint': 17.0,
                'time_until': b'\x00',
                'valve_position': 0,
            },
            b'0b04be': {
                '?1': 246,
                'date_until': b'\x00\xdb',
                'flags_1': 18,
                'flags_2': 24,
                'len': 11,
                'rf_address': b'0b04be',
                'temperature_setpoint': 17.0,
                'time_until': b'\x00',
                'valve_position': 0,
            },
        },
        handle_output_L(
            b'CwsEvvYSGAAiANsACwi20lwSGAAiAOEABgG0kVwSEF=='
        )
    )
