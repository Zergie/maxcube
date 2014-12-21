# -*- coding: utf-8 -*-
import base64
import binascii

import datetime
from pprint import pprint

VL  = object() # variable length (length found in first bit)
ALL = object() # no length restriction
T0  = object() # decode until 0x00

class temp(object):         __slots__ = ()
class temp_offset(object):  __slots__ = ()
class temppair(object):     __slots__ = ()
class percent(object):      __slots__ = ()

class hexdate(object):      __slots__ = ()
class hextime(object):      __slots__ = ()
class dailyprogram(object): __slots__ = ()

class PropertyContainer(object): pass


def parse(field, data_already_parsed, raw_bytes):
    field.data_already_parsed = data_already_parsed
    return field.parse(raw_bytes)


class ffield(object): 
    def __init__(self, name, length, type):
        self.name   = name
        self.length = length
        self.type   = type

    def parse(self, raw_bytes):
        if self.length == ALL:
            ret = self.decode(raw_bytes, len(raw_bytes))
        else:
            if self.length == VL:
                byte_length = int(raw_bytes[0]) + 1
                byte_data   = raw_bytes[1:byte_length]
            elif self.length == T0:
                byte_length = 0

                for i in raw_bytes:
                    byte_length += 1
                    if i == 0x00: break

                byte_data   = raw_bytes[0:byte_length-1]
            else:
                byte_length = self.length
                byte_data   = raw_bytes[0:byte_length]

            ret = self.decode(byte_data, byte_length)
        return ret

    def decode(self, byte_data, byte_length):
        #print('name=', self.name, )

        if self.type is str:
            decoded_data = byte_data.decode()
        elif self.type is int:
            decoded_data = int.from_bytes(byte_data, byteorder='big')
        elif self.type is temp:
        	decoded_data = int.from_bytes(byte_data, byteorder='big') / 2
        elif self.type is temp_offset:
        	decoded_data = int.from_bytes(byte_data, byteorder='big') / 2 - 3.5
        elif self.type is percent:
        	decoded_data = int.from_bytes(byte_data, byteorder='big') * (100 / 255)
        elif self.type is bytes:
            decoded_data = binascii.b2a_hex(byte_data)
        elif self.type is datetime.date:
            decoded_data = datetime.date(2000 + int(byte_data[0:2], 16), int(byte_data[2:4], 16), int(byte_data[4:6], 16))
        elif self.type is datetime.time:
            decoded_data = datetime.time(int(byte_data[0:2], 16), int(byte_data[2:4], 16))
        elif self.type is temppair:
            decoded_data = None # todo 
        elif self.type is hexdate:
            decoded_data = None # todo
        elif self.type is hextime:
            decoded_data = None # todo
        elif self.type is dailyprogram:
            decoded_data = []

            for i in range(0, byte_length, 2):
                print('byte_data', byte_data[i:])
                pair  = byte_data[i:i+2]

                temperature  = int((pair[0] >> 1) / 2)
                minutes = (((pair[0] & 0x01) << 8) | pair[1]) * 5

                if minutes != 1440 and temperature != 17:
                    time = (datetime.datetime(2000,1,1) + datetime.timedelta(minutes=minutes)).time()
                    decoded_data.append([temperature, time])
        
        #pprint(decoded_data)
        return byte_length, {self.name : decoded_data}


class ffixed(ffield):
    def __init__(self, name, fixed_data):
        self.fixed_data = fixed_data

        if isinstance(self.fixed_data, int):
            ffield.__init__(self, name, 1, type(fixed_data))
        else:
            ffield.__init__(self, name, len(fixed_data), type(fixed_data))
    def decode(self, byte_data, byte_length):
        return byte_length, {self.name : self.fixed_data}


class fbase64(object):
    def __init__(self, *fields):
        self.fields = fields
    def parse(self, raw_bytes):
        decoded = base64.decodebytes(raw_bytes)
        start = 0
        data_decoded  = {}

        for obj in self.fields:
            parsed_length, parsed_data = parse(obj,  data_decoded, decoded[start:])

            data_decoded.update(parsed_data)
            start += parsed_length

            if start >= len(decoded):
                break

        data_decoded['unknown_base64'] = decoded[start:]
        if len(data_decoded['unknown_base64']) == 0:
            del(data_decoded['unknown_base64'])
        else:
            print('unknown_base64=', data_decoded['unknown_base64'])

        return len(raw_bytes), data_decoded


class fmultiple(object):
    def __init__(self, name, *fields):
        self.name   = name
        self.fields = fields
    def parse(self, raw_bytes):
        count = int(raw_bytes[0])
        start = 1
        items = []

        for j in range(0, count):
            data = PropertyContainer()
            for obj in self.fields:
                parsed_length, parsed_data = parse(obj,  data.__dict__, raw_bytes[start:])

                data.__dict__.update(parsed_data)
                start += parsed_length
            items.append(data)

        return start, {self.name : items}


class fchoose(object):
    def __init__(self, name, decision_dict):
        self.name          = name
        self.decision_dict = decision_dict
    def parse(self, raw_bytes):
        index    = self.data_already_parsed[self.name]
        obj_list = self.decision_dict[index]
        
        start = 0
        data_decoded  = {}
        for obj in obj_list:
            byte_data = raw_bytes[start:]
            bytes_parsed, parsed_data = parse(obj,  data_decoded, byte_data)

            data_decoded.update(parsed_data)
            start += bytes_parsed

        return start, data_decoded


class fcsv(object):
    def __init__(self, *fields):
        self.fields = fields
    def parse(self, raw_bytes):
        parts   = raw_bytes.split(b',')

        bytes_decoded = -1
        data_decoded  = {}
        for i in range(0, len(self.fields)):
            obj = self.fields[i]
            
            count, data = parse(obj,  data_decoded, parts[i].strip())

            data_decoded.update(data)
            bytes_decoded += len(parts[i]) + 1
        return bytes_decoded, data_decoded



class MessageTyp(object): 
    def __init__(self, raw_bytes=None):
        if raw_bytes != None:
            self._parse(raw_bytes)

    def _parse(self, raw_bytes):
        start = 0

        for obj in self.fields:
            byte_data = raw_bytes[start:]
            bytes_parsed, parsed_data = parse(obj,  self.__dict__, byte_data)
            
            for k, v in parsed_data.items():
                self.__dict__[k] = v

            start += bytes_parsed

        self.unknown_raw = raw_bytes[start:]
        if len(self.unknown_raw) == 0:
            del(self.unknown_raw)
        else:
            print('unknown_raw=', self.unknown_raw)

        # cleanup __dict__
        del(self.fields)
        try:
            del(self._end)
        except:
            pass
