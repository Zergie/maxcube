# -*- coding: utf-8 -*-
from maxcube.client_commands import *
from maxcube.cube_commands import *

def parse(raw_data):
    ret = []
    for line in raw_data.split(b'\r\n'):
        if len(line) > 0:
            ret.append(handle_output(line + b'\r\n'))
    return ret


def handle_output(line):
    print('\nparseing:', line)
    msg_type = chr(line[0]) + '_'
    cls = None

    for c in MessageTyp.__subclasses__():
        if c.__name__.startswith(msg_type):
            cls = c
            break

    if cls != None:
        message = c()
        message.parse(line)
        return message
    else:
        return None


def compose(cls, values={}):
    msg = cls()
    return msg.compose(values)