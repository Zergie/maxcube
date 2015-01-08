# -*- coding: utf-8 -*-
import base64
import binascii

import datetime
from math import log
from pprint import pprint
from maxcube.constants import *

class time5(object):           __slots__ = ()
class temp(object):            __slots__ = ()
class temp2(object):           __slots__ = ()
class temp_offset(object):     __slots__ = ()
class percent(object):         __slots__ = ()
class boost(object):           __slots__ = ()
class decalcification(object): __slots__ = ()
class weeklyprogram(object):   __slots__ = ()

class PropertyContainer(object): pass


def parse(field, data_already_parsed, raw_bytes):
    field.data_already_parsed = data_already_parsed
    return field.parse(raw_bytes)


def optional(field):
    field.optional = True
    return field


class ffield(object): 
    def __init__(self, name, length, type):
        self.name     = name
        self.length   = length
        self.type     = type
        self.optional = False

        decode_old, encode_old = (None, None)
        if 'decode' in dir(self): decode_old = self.decode
        if 'encode' in dir(self): encode_old = self.encode

        if self.type is str:
            self.decode, self.encode = (self.decode_str           , self.encode_str)
        elif self.type is int:
            self.decode, self.encode = (self.decode_int           , self.encode_int)
        elif self.type is temp:
            self.decode, self.encode = (self.decode_temp          , self.encode_temp)
        elif self.type is temp2:
            self.decode, self.encode = (self.decode_temp2         , self.encode_temp2)
        elif self.type is temp_offset:
            self.decode, self.encode = (self.decode_temp_offset   , self.encode_temp_offset)
        elif self.type is percent:
            self.decode, self.encode = (self.decode_percent       , self.encode_percent)
        elif self.type is bytes:
            self.decode, self.encode = (self.decode_bytes         , self.encode_bytes)
        elif self.type is datetime.date:
            self.decode, self.encode = (self.decode_date          , self.encode_date)
        elif self.type is datetime.time:
            self.decode, self.encode = (self.decode_time          , self.encode_time)
        elif self.type is time5:
            self.decode, self.encode = (self.decode_time5         , self.encode_time5)
        elif self.type is weeklyprogram:
            self.decode, self.encode = (self.decode_weeklyprogram , self.encode_weeklyprogram)
        elif self.type is boost:
            self.decode, self.encode = (self.decode_boost         , self.encode_boost)
        elif self.type is decalcification:
            self.decode, self.encode = (self.decode_decalcification, self.encode_decalcification)

        if decode_old != None: self.decode = decode_old
        if encode_old != None: self.encode = encode_old

    def compose(self, values):
        if self.optional and not self.name in values:
            return b''
        elif self.optional and values[self.name] == None:
            return b''
        else:
            msg = self.encode(values)
            try:
                length = self.length
            except:
                length = None

            if length == T0:
                return msg + bytes([0x00])
            elif length == VL:
                return bytes([len(msg)]) + msg
            else:
                return msg

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


    def decode_str(self, byte_data, byte_length):
        return byte_length, {self.name : byte_data.decode()}
    def encode_str(self, values):
        return str(values[self.name]).encode('utf-8')

    def decode_int(self, byte_data, byte_length):
        return byte_length, {self.name : int.from_bytes(byte_data, byteorder='big')}
    def encode_int(self, values):
        return bytes([values[self.name]])

    def decode_temp(self, byte_data  , byte_length):
        value = int.from_bytes(byte_data, byteorder='big')
        temperature = (value & 0b00111111) / 2
        
        if ((value & vacation.value) == 0b10000000): mode = vacation
        elif ((value & auto.value) == 0b00000000):   mode = auto
        elif ((value & manual.value) == 0b01000000): mode = manual
        elif ((value & boost.value) == 0b11000000):  mode = boost

        if temperature   == ON.value:  temperature = ON
        elif temperature == OFF.value: temperature = OFF

        if mode == auto:
            return byte_length, { self.name           : temperature}
        else:
            return byte_length, { self.name           : temperature, 
                                  self.name + '_mode' : mode}
    def encode_temp(self, values  ):
        value = int(values[self.name] * 2)
        try:
            mode = values[self.name + '_mode']
        except:
            mode = auto

        if mode == vacation: value |= vacation.value
        elif mode == auto:   value |= auto.value
        elif mode == manual: value |= manual.value
        elif mode == boost:  value |= boost.value
        
        return bytes([value])

    def decode_temp2(self, byte_data  , byte_length):
        value = int.from_bytes(byte_data, byteorder='big') / 4
        return byte_length, { self.name           : value}
    def encode_temp2(self, values  ):
        value = int(values[self.name] * 4) 
        return bytes([value])

    def decode_temp_offset(self, byte_data, byte_length):
        decoded_data = int.from_bytes(byte_data, byteorder='big') / 2 - 3.5
        return byte_length, {self.name : decoded_data}
    def encode_temp_offset(self, values):
        value = int(values[self.name] * 2 - 3.5)
        return bytes([value])

    def decode_percent(self, byte_data, byte_length):
        decoded_data = int.from_bytes(byte_data, byteorder='big') * (100 / 255)
        return byte_length, {self.name : decoded_data}
    def encode_percent(self, values):
        value = int(values[self.name] * (255 / 100))
        return bytes([value])

    def decode_bytes(self, byte_data, byte_length):
        return byte_length, {self.name : binascii.hexlify(byte_data)}
    def encode_bytes(self, values):
        return binascii.unhexlify(values[self.name])

    def decode_date(self, byte_data, byte_length):
        if byte_data == b'\x00\x00':
            decoded_data = None
        elif byte_length == 2:
            day   = (byte_data[0] & 0b00111111)
            month = ((byte_data[0] & 0b11100000) >> 4) + ((byte_data[1] & 0b10000000) >> 7)
            year   = (byte_data[1] & 0b00011111)
            
            try:
                decoded_data = datetime.date(2000 + year, month, day)
            except:
                print(list(byte_data), (2000 + year, month, day))
                decoded_data = None # what does this mean?
        else:
            decoded_data = datetime.date(2000 + int(byte_data[0:2], 16), int(byte_data[2:4], 16), int(byte_data[4:6], 16))
        return byte_length, {self.name : decoded_data}
    def encode_date(self, values):
        if self.length == 2:
            value  = [0x00, 0x00]
            value[0] |= (values[self.name].day & 0b00111111)
            value[0] |= (values[self.name].month & 0b00000001) << 7
            value[0] |= (values[self.name].month & 0b00001110) << 4
            value[1] |= ((values[self.name].year - 2000) & 0b00011111)
            return bytes(value)
        else:
            return binascii.hexlify(bytes([values[self.name].year - 2000, values[self.name].month, values[self.name].day]))
        

    def decode_time(self, byte_data, byte_length):
        if byte_data == b'\x00':
            decoded_data = None
        elif byte_length == 1:
            decoded_data = (datetime.datetime(2000,1,1) + datetime.timedelta(minutes=byte_data[0]*30)).time()
        else:
            decoded_data = datetime.time(int(byte_data[0:2], 16), int(byte_data[2:4], 16))
        return byte_length, {self.name : decoded_data}
    def encode_time(self, values):
        if self.length == 1:
            value = int((values[self.name].hour * 60 + values[self.name].minute) / 30)
            return bytes([value])
        else:
            return binascii.hexlify(bytes([values[self.name].hour, values[self.name].minute]))

    def decode_time5(self, byte_data, byte_length):
        decoded_data = (datetime.datetime(2000,1,1) + datetime.timedelta(minutes=byte_data[0]*5)).time()
        return byte_length, {self.name : decoded_data}
    def encode_time5(self, values):
        value = int((values[self.name].hour * 12 + values[self.name].minute) / 5)
        return bytes([value])


    def decode_boost(self, byte_data, byte_length):
        time  = ((byte_data[0] & 0b11100000) >> 5) * 5
        valve = (byte_data[0] & 0b00011111) / 20 * 100

        return byte_length, {self.name + '_time'  : time,
                             self.name + '_valve' : valve}
    def encode_boost(self, values):
        valve = values[self.name + '_valve'] * (20 / 100)
        value |= ((values[self.name + '_time'] / 5) << 5)
        return bytes([value])

    def decode_decalcification(self, byte_data, byte_length):
        day  = ((byte_data[0] & 0b11100000) >> 5)
        hour = (byte_data[0]  & 0b00011111)

        return byte_length, {self.name + '_day'  : ['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri'][day],
                             self.name + '_hour' : datetime.time(hour, 0)}
    def encode_decalcification(self, values):
        valve = 0x00
        return bytes([value])
        


    def decode_weeklyprogram(self, byte_data, byte_length):
        decoded_data = {}

        for day in ['sat', 'sun', 'mon', 'tue', 'wed', 'thu', 'fri']:
            decodec_data_day = []
            
            for i in range(0, 13):
                pair  = byte_data[(i*2):(i*2)+2]

                temperature  = int((pair[0] >> 1) / 2)
                minutes = (((pair[0] & 0x01) << 8) | pair[1]) * 5

                if minutes != 1440 and temperature != 17:
                    time = (datetime.datetime(2000,1,1) + datetime.timedelta(minutes=minutes)).time()
                    decodec_data_day.append([temperature, time])

            decoded_data[day] = decodec_data_day
    
        return byte_length, {self.name : decoded_data}
    def encode_weeklyprogram(self, values):
        pass # todo


class fflags(ffield):
    def __init__(self, *fields):
        self.fields = fields
    def parse(self, raw_bytes):
        data_decoded  = {}

        for i in self.fields:
            name   = i[0]
            mask   = i[1]
            values = i[2]
            shift = int(log((1 + (mask ^ (mask-1))) >> 1, 2))

            value  = (raw_bytes[0] & mask) >> shift

            data_decoded[name] = values[value]
        
        return 1, data_decoded
        

class ffixed(ffield):
    def __init__(self, name, fixed_data):
        self.fixed_data = fixed_data

        if isinstance(self.fixed_data, int):
            ffield.__init__(self, name, 1, type(fixed_data))
        else:
            ffield.__init__(self, name, len(fixed_data), type(fixed_data))
    def compose(self, values):
        if isinstance(self.fixed_data, int):
            return bytes([self.fixed_data])
        else:
            return bytes(self.fixed_data)
    def decode(self, byte_data, byte_length):
        if bytes(self.fixed_data) != byte_data:
            print(self.name, self.fixed_data, '!=', byte_data)
        return byte_length, {self.name : self.fixed_data}


class fbase64(ffield):
    def __init__(self, *fields):
        self.fields   = fields
        self.optional = False
    def compose(self, values):
        msg = b''
        for obj in self.fields:
            msg += obj.compose(values)
        return base64.encodebytes(msg).replace(b'\n', b'')
    def parse(self, raw_bytes):
        decoded = base64.decodebytes(raw_bytes)

        if self.optional and len(decoded) == 0:
            return 0, {}
        else:
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

            return len(raw_bytes) - 2, data_decoded


class fmultiple(ffield):
    def __init__(self, name, count, *fields):
        self.name   = name
        self.count  = count
        self.fields = fields
    def compose(self, values):
        if self.count == VL:
            msg = bytes([len(values[self.name])])
        else:
            msg = b''
        for i in values[self.name]:
            for obj in self.fields:
                msg += obj.compose(i)
        return msg
    def parse(self, raw_bytes):
        if self.count == VL:
            count = int(raw_bytes[0])
            ret = self.decode(1, raw_bytes, count)
        elif self.count == ALL:
            ret = self.decode(0, raw_bytes, 999)
        else:
            ret = self.decode(1, raw_bytes, self.count)
        return ret
    def decode(self, start, byte_data, count):
        items = []

        for j in range(0, count):
            data = PropertyContainer()
            for obj in self.fields:
                parsed_length, parsed_data = parse(obj,  data.__dict__, byte_data[start:])
                data.__dict__.update(parsed_data)
                start += parsed_length
            items.append(data)

            if start >= len(byte_data):
                break

        return start, {self.name : items}


class fchoose(ffield):
    def __init__(self, name, decision_dict):
        self.name          = name
        self.decision_dict = decision_dict
        self.optional      = False
    def encode(self, values):
        index = values[self.name]

        msg = b''
        for obj in self.decision_dict[index]:
            msg += obj.compose(values)

        return msg 
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


class fcsv(ffield):
    def __init__(self, *fields):
        self.fields   = fields
        self.optional = False
    def compose(self, values):
        msg = b''
        for obj in self.fields:
            msg += obj.compose(values) + b','
        return msg[:-1]
    def parse(self, raw_bytes):
        parts   = raw_bytes.split(b',')
        
        if self.optional and len(parts) <= 1:
            return 0, {}
        else:
            bytes_decoded = -1
            data_decoded  = {}
            for i in range(0, len(self.fields)):
                obj = self.fields[i]
                
                count, data = parse(obj,  data_decoded, parts[i].strip())

                data_decoded.update(data)
                bytes_decoded += len(parts[i]) + 1
            return bytes_decoded, data_decoded



class MessageTyp(object):
    def __init__(self):
        pass

    def compose(self, values={}):
        msg = b''
        for obj in self.fields:
            msg += obj.compose(values)
        return msg

    def parse(self, raw_bytes):
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

        # cleanup __dict__
        del(self.fields)
        try:
            del(self._end)
        except:
            pass
