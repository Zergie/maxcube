# -*- coding: utf-8 -*-
from nose import tools

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'maxcube'))

import datetime

from maxcube import composing

def test_composing():
	tools.assert_equal(b's:AARAAAAAAP4wAaiLix8=\r\n',
						composing.compose_s([0x00, 0xfe, 0x30], 1, 20, 2, datetime.date(2011, 9, 11), datetime.time(15, 30)))

	tools.assert_equal([0x00, 0x04, 0x40, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x30, 0x01, 0x00],
						composing.compile_s([0x00, 0xfe, 0x30], 1, 0, 0, None, None))

	tools.assert_equal(b's:AARAAAAAAP4wAQA=\r\n',
						composing.compose_s([0x00, 0xfe, 0x30], 1, 0, 0, None, None))

	tools.assert_equal([0x00, 0x04, 0x40, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x30, 0x01, 0x6C],
						composing.compile_s(bytes([0x00, 0xfe, 0x30]), 1, 22, 1, None, None))
