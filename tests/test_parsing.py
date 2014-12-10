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

    tools.assert_equal(
        {
            'rf_address': b'0b04be',
            'duration_boost': 80,
            'temperature_offset': 0.0,
            'test_result': 255,
            'type': 2,
            'decalcification': b'\x87',
            'serial': b'KEQ0571674',
            'temperature_eco': 16.5,
            'room_id': 1,
            'data_len': 210,
            'valve_offset': 0.0,
            'duration_window_open': 3,
            'temperature_setpoint_max': 30.5,
            'valve_maximum': 100.0,
            'program': b'DN\\fX\xfcU\x14E E E E E E E E E DN\\fX\xfcU\x14E E E E E E E E E DN\\fX\xfcU\x14E E E E E E E E E DN\\fX\xfcU\x14E E E E E E E E E DN\\fX\xfcU\x14E E E E E E E E E DN\\fX\xfcU\x14E E E E E E E E E DN\\fX\xfcU\x14E E E E E E E E E ',
            'temperature_setpoint_min': 4.5,
            'fw_version': 16,
            'temperature_comfort': 22.0,
            'temperature_window_open': 12.0
        },
        handle_output_C(
            b'0b04be,0gsEvgIBEP9LRVEwNTcxNjc0LCE9CQcYA1CH/wBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZY/FUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlj8VRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWPxVFEUgRSBFIEUgRSBFIEUgRSBFIA==',
        )
    )

    tools.assert_equal(
        {
            'duration_boost': 80,
            'room_id': 2,
            'test_result': 0,
            'valve_offset': 0.0,
            'temperature_setpoint_max': 30.5,
            'valve_maximum': 100.0,
            'temperature_setpoint_min': 4.5,
            'data_len': 210,
            'temperature_offset': 0.0,
            'temperature_eco': 16.5,
            'temperature_window_open': 12.0,
            'temperature_comfort': 23.0,
            'fw_version': 16,
            'program': b'DN\\f[\x08U\x14E E E E E E E E E DN\\f[\x08U\x14E E E E E E E E E DN\\f[\x08U\x14E E E E E E E E E DN\\f[\x08U\x14E E E E E E E E E DN\\f[\x08U\x14E E E E E E E E E DN\\f[\x08U\x14E E E E E E E E E DN\\f[\x08U\x14E E E E E E E E E ',
            'type': 2,
            'rf_address': b'08b6d2',
            'duration_window_open': 3,
            'decalcification': b'\x0c',
            'serial': b'KEQ0634607'
        },
        handle_output_C(
            b'08b6d2,0gi20gICEABLRVEwNjM0NjA3LiE9CQcYA1AM/wBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIEROXGZbCFUURSBFIEUgRSBFIEUgRSBFIEUgRE5cZlsIVRRFIEUgRSBFIEUgRSBFIEUgRSBETlxmWwhVFEUgRSBFIEUgRSBFIEUgRSBFIA=='
        )
    )

    tools.assert_equal(
        {
            'data_len': 17,
            'rf_address': b'01b491',
            'serial': b'JEQ0305205',
            'type': 5,
            'fw_version': 18,
            'room_id': 0,
            'test_result': 15
        },
        handle_output_C(
            b'C:01b491,EQG0kQUAEg9KRVEwMzA1MjA1'
        )
    )


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
