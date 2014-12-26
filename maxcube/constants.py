# -*- coding: utf-8 -*-

# consts for parsing
VL  = object() # variable length (length found in first bit)
ALL = object() # no length restriction
T0  = object() # decode until 0x00


# temperature values
ON  = object()
OFF = object()

# temperature modes
auto     = object()
manual   = object()
vacation = object()
boost    = object()