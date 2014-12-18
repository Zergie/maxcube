# -*- coding: utf-8 -*-
from nose import tools

import os.path
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'maxcube'))

from maxcube import objects
from maxcube import parsing
from maxcube import output

from test_parsing import RAW_DATA


def test_integration():
    cube = objects.from_parsed_data(parsing.start(RAW_DATA))
    tools.assert_equal('0113', cube.firmware_version)
    tools.assert_equal('JEQ0543545', cube.serial)
    tools.assert_equal('03f6c9', cube.address)

    tools.assert_equal(2, len(cube.rooms))
    tools.assert_equal(3, len(cube.devices))
