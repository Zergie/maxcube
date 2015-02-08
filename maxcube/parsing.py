# -*- coding: utf-8 -*-
from maxcube.cube_commands import *
from maxcube.client_commands import *

def parse(raw_data):
    ret = []
    for line in raw_data.split(b'\r\n'):
        if len(line) > 0:
            ret.append(handle_output(line + b'\r\n'))
    return ret


def handle_output(line):
    print('\nparseing:', line)
    msg_type = chr(line[0]) + '_'

    for c in MessageTyp.__subclasses__():
        if c.__name__.startswith(msg_type):
            message = c()
            message.parse(line)
            return message

    return None


def compose(cls, values={}):
    msg = cls()
    return msg.compose(values)