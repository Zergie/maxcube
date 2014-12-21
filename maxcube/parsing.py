# -*- coding: utf-8 -*-
import base64
import binascii
from pprint import pprint
from io import BytesIO
from collections import defaultdict

import datetime

# concept start
class PropertyContainer(object):
    def __init__(self):
        pass


class FieldTyp(object): 
    def __init__(self, name, length=-1):
        self.name   = name
        self.length = length
    def parse(self, raw_bytes):
        if self.length == -1:
            ret = self.decode(raw_bytes)
        else:
            ret = self.decode(raw_bytes[:self.length])
        #print(ret)
        return ret

class pFixed   (FieldTyp):
    def __init__(self, name, fixed_data):
        self.fixed_data = fixed_data
        FieldTyp.__init__(self, name)
    def decode(self, raw_bytes):
        if isinstance(self.fixed_data, int):
            return 1, {self.name: self.fixed_data}
        else:
            return len(self.fixed_data), {self.name: self.fixed_data}

class pString(FieldTyp):
    def decode(self, raw_bytes):
        return len(raw_bytes), {self.name: raw_bytes.decode()}

class pStringVL(FieldTyp):
    def decode(self, raw_bytes):
        length = int(raw_bytes[0])
        return length+1, {self.name: raw_bytes[1:1+length].decode()}

class pDate(FieldTyp):
    def decode(self, raw_bytes):
        return len(raw_bytes), {self.name: datetime.date(2000 + int(raw_bytes[0:2], 16), int(raw_bytes[2:4], 16), int(raw_bytes[4:6], 16))}

class pTime(FieldTyp):
    def decode(self, raw_bytes):
        return len(raw_bytes), {self.name: datetime.time(int(raw_bytes[0:2], 16), int(raw_bytes[2:4], 16))}

class pByte(FieldTyp):
    def decode(self, raw_bytes):
        return len(raw_bytes), {self.name: binascii.b2a_hex(raw_bytes)}

class pInteger(FieldTyp):
    def decode(self, raw_bytes):
        return len(raw_bytes), {self.name: int.from_bytes(raw_bytes, byteorder='big')}

class pTempPair (FieldTyp):
    def decode(self, raw_bytes):
        pass
class pHexDate  (FieldTyp):
    def decode(self, raw_bytes):
        pass
class pHexTime  (FieldTyp):
    def decode(self, raw_bytes):
        pass

class pBase64   (FieldTyp):
    def __init__(self, *fields):
        self.fields = fields
    def parse(self, raw_bytes):
        decoded = base64.decodebytes(raw_bytes)

        start = 0
        data  = {}
        for obj in self.fields:
            bytes_parsed, parsed_data = obj.parse(decoded[start:])

            data.update(parsed_data)
            start += bytes_parsed

            if start >= len(decoded):
                break
        return len(raw_bytes), data

class pMultiple(FieldTyp):
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
                bytes_parsed, parsed_data = obj.parse(raw_bytes[start:])

                data.__dict__.update(parsed_data)
                start += bytes_parsed
            items.append(data)

        return start, {self.name : items}

class pCsv(FieldTyp):
    def __init__(self, *fields):
        self.fields = fields
    def parse(self, raw_bytes):
        parts   = raw_bytes.split(b',')

        bytes_decoded = -1
        data_decoded  = {}
        for i in range(0, len(self.fields)):
            obj = self.fields[i]
            
            count, data = obj.parse(parts[i].strip())

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
            bytes_parsed, parsed_data = obj.parse(raw_bytes[start:])
            
            for k, v in parsed_data.items():
                self.__dict__[k] = v

            start += bytes_parsed


class H_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [pFixed('msg_type', b'H:')   ,
                       pCsv(
                            pString('serial'            ),
                            pString('rf_address'        ),
                            pString('firmware_version'  ),
                            pString('unknown'           ),
                            pString('http_connection_id'),
                            pString('duty_cycle'        ),
                            pString('free_memory_slots' ),
                            pDate  ('cube_date'         ),
                            pTime  ('cube_time'         ),
                            pString('clock_set'         ),
                            pString('unknown2'          )
                            ),
                       pFixed('_end', b'\r\n') ]
        MessageTyp.__init__(self, raw_bytes)

class C_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [pFixed('msg_type', b'C:')   ,
                       pCsv(
                           ),
                       pFixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)

class M_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [pFixed('msg_type', b'M:')   ,
                       pCsv(                                            # todo: fcsv( ... )
                            pFixed('unknown' , '00'),
                            pFixed('unknown2', '01'),
                            pBase64(                                    # todo: fbase64( ... )
                                   pFixed('magicbyte', 0x56          ), # todo: fmagic('magicbyte', 0x56)
                                   pFixed('version'  , 0x02          ),
                                   pMultiple('rooms'                  ,
                                             pInteger('id'       ,  1), # todo: ffield('id'       ,  1,  int)
                                             pStringVL('name'        ), # todo: ffield('name'     , VL,  str)
                                             pByte('rf_address'  ,  3)  # todo: ffield('rf_adress',  3,  byte)
                                            ),,  3, byte
                                   pMultiple('devices'                ,
                                             pInteger('type'     ,  1),
                                             pByte('rf_address'  ,  3),
                                             pString('serial'    , 10), # todo: ffield('serial'   , 10,  str)
                                             pStringVL('name'        ), # todo: ffield('name'     , VL,  str)
                                             pInteger('room_id'  ,  1)
                                            ),
                                   pInteger('unknown3')
                                   )
                            ),
                       pFixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)

class L_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [pFixed('msg_type', b'L:')   ,
                       pCsv(
                           ),
                       pFixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)

#class s_Message(MessageTyp):
#    def __init__(self):
#        self.fields = {'msg_type'            : pFixed('s:')    ,
#                        pBase64('magic'     ,  pFixed([0x00, 0x04, 0x40, 0x00, 0x00, 0x00]) ,
#                                'rf_address',  pHex()          ,
#                                'room_id'   ,  pHex()          ,
#                                'temp_pair' ,  pTempPair()     ,
#                                'date'      ,  pHexDate(0, 1)  ,
#                                'time'      ,  pHexTime(0, 1)) ,
#                       ''                   :  pFixed('\r\n')  }
#                      }

# concept end

def start(raw_data):
    ret = []
    for line in raw_data.split(b'\r\n'):
        ret.append(handle_output(line + b'\r\n'))
    return ret

def handle_output(line):
    if not line:
        return None, None
    elif len(line) == 2:
        return None, None

    print(line[0:10], len(line))
    msg_type = chr(line[0]) + '_'
    
    for c in MessageTyp.__subclasses__():
        if c.__name__.startswith(msg_type):
            break

    message = c(line)
    print(message)
    return message


def handle_output_H(line):
    serial, rf_address, firmware_version, unknown, http_connection_id, duty_cycle, free_memory_slots, cube_date, cube_time, clock_set, unknown2  = line.decode().strip().split(',')

    cube_date = datetime.date(2000 + int(cube_date[0:2], 16), int(cube_date[2:4], 16), int(cube_date[4:6], 16))
    cube_time = datetime.time(int(cube_time[0:2], 16), int(cube_time[2:4], 16))
    return {
        'serial': serial,
        'rf_address': rf_address,
        'firmware_version': firmware_version,
        '?1' : unknown,
        'http_connection_id' : http_connection_id,
    	'duty_cycle' : duty_cycle,
		'free_memory_slots' : free_memory_slots,
        'cube_date' : cube_date,
        'cube_time' : cube_time,
    	'clock_set' : clock_set,
    	'?2' : unknown2
    }








def handle_output_M(line):
    position = 0
    data = {}
    _1, _2, encoded = line.strip().split(b',', 2)
    decoded = BytesIO(base64.decodebytes(encoded))

    data['magicbyte'] = ord(decoded.read(1)) # Meta Data Magic. Should always be 0x56
    data['version'] = ord(decoded.read(1)) # Meta data version. Should always be 0x02

    # Rooms
    data['room_count'] = ord(decoded.read(1))
    data['rooms'] = {}
    for i in range(data['room_count']):
        room = {}
        room['id'] = ord(decoded.read(1))
        room['name_len'] = ord(decoded.read(1))
        room['name'] = decoded.read(room['name_len'])
        room['rf_address'] = binascii.b2a_hex(decoded.read(3))
        data['rooms'][room['id']] = room

    # Devices
    data['devices_count'] = ord(decoded.read(1))
    data['devices'] = []
    for i in range(data['devices_count']):
        device = {}
        device['type'] = ord(decoded.read(1))
        device['rf_address'] = binascii.b2a_hex(decoded.read(3))
        device['serial'] = decoded.read(10)
        device['name_len'] = ord(decoded.read(1))
        device['name'] = decoded.read(device['name_len'])
        device['room_id'] = ord(decoded.read(1))

        data['devices'].append(device)

    # Unknown byte
    data['?2'] = decoded.read(1)

    return data

def handle_output_C(line):
    data = {}
    prefix, encoded = line.strip().split(b',', 1)
    decoded = BytesIO(base64.decodebytes(encoded))
    data['data_len'] = ord(decoded.read(1))
    data['rf_address'] = binascii.b2a_hex(decoded.read(3))
    data['type'] = ord(decoded.read(1))
    data['room_id'] = ord(decoded.read(1))
    data['fw_version'] = ord(decoded.read(1))
    data['test_result'] = ord(decoded.read(1))
    data['serial'] = decoded.read(10)
    if data['type'] == 2 or data['type'] == 1:
        # RadiatorThermostat
        data['temperature_comfort'] = ord(decoded.read(1)) / 2
        data['temperature_eco'] = ord(decoded.read(1)) / 2
        data['temperature_setpoint_max'] = ord(decoded.read(1)) / 2
        data['temperature_setpoint_min'] = ord(decoded.read(1)) / 2
        data['temperature_offset'] = (ord(decoded.read(1)) / 2) - 3.5
        data['temperature_window_open'] = ord(decoded.read(1)) / 2
        data['duration_window_open'] = ord(decoded.read(1))
        data['duration_boost'] = ord(decoded.read(1)) # TODO
        data['decalcification'] = decoded.read(1) # TODO
        data['valve_maximum'] = ord(decoded.read(1)) * (100 / 255)
        data['valve_offset'] = ord(decoded.read(1)) * (100 / 255)
        data['program_sat'] = handle_output_program(decoded.read(26))
        data['program_sun'] = handle_output_program(decoded.read(26))
        data['program_mon'] = handle_output_program(decoded.read(26))
        data['program_tue'] = handle_output_program(decoded.read(26))
        data['program_wed'] = handle_output_program(decoded.read(26))
        data['program_thu'] = handle_output_program(decoded.read(26))
        data['program_fri'] = handle_output_program(decoded.read(26))
    elif data['type'] == 3:
        # WallThermostat
        data['temperature_comfort'] = ord(decoded.read(1)) / 2
        data['temperature_eco'] = ord(decoded.read(1)) / 2
        data['temperature_setpoint_max'] = ord(decoded.read(1)) / 2
        data['temperature_setpoint_min'] = ord(decoded.read(1)) / 2
        data['program'] = decoded.read(182) # TODO

    return data

def handle_output_program(raw_bytes):
    ret = []

    for i in range(0,len(raw_bytes),2):
        pair  = raw_bytes[i:i+2]

        temp  = int((pair[0] >> 1) / 2)
        minutes = (((pair[0] & 0x01) << 8) | pair[1]) * 5

        if minutes != 1440 and temp != 17:
            time = (datetime.datetime(2000,1,1) + datetime.timedelta(minutes=minutes)).time()
            ret.append([temp, time])
    return ret


def handle_output_L(line):
    data = {}
    encoded = line.strip()
    decoded = BytesIO(base64.decodebytes(encoded))
    data = {}
    while True:
        device = {}
        try:
            device['len'] = ord(decoded.read(1))
        except TypeError:
            break
        device['rf_address'] = binascii.b2a_hex(decoded.read(3))
        device['?1'] = ord(decoded.read(1))
        
        device['flags_1'] = ord(decoded.read(1)) 
        # bits for flags_1:
        # bit 4     Valid              0=invalid;1=information provided is valid
        # bit 3     Error              0=no; 1=Error occurred
        # bit 2     Answer             0=an answer to a command,1=not an answer to a command
        # bit 1     Status initialized 0=not initialized, 1=yes
        #      
        # 12  = 00010010b
        #     = Valid, Initialized

        device['flags_2'] = ord(decoded.read(1)) 
        # bits for flags_2:
        # bit 7     Battery       1=Low
        # bit 6     Linkstatus    0=OK,1=error
        # bit 5     Panel         0=unlocked,1=locked
        # bit 4     Gateway       0=unknown,1=known
        # bit 3     DST setting   0=inactive,1=active
        # bit 2     Not used
        # bit 1,0   Mode         00=auto/week schedule
        #                        01=Manual
        #                        10=Vacation
        #                        11=Boost   
        # 1A  = 00011010b
        #     = Battery OK, Linkstatus OK, Panel unlocked, Gateway known, DST active, Mode Vacation.
        if device['len'] > 6:
            device['valve_position'] = ord(decoded.read(1)) # Valve position in %
            device['temperature_setpoint'] = ord(decoded.read(1)) / 2
            device['date_until'] = decoded.read(2) # todo: convert to datetime.datetime
            device['time_until'] = decoded.read(1) # todo: convert to datetime.time
        data[device['rf_address']] = device
    return data

def handle_output_default(line):
    print('handling default')
    print(line)

OUTPUT_SIGNATURES = {
    b'H:': handle_output_H,
    b'M:': handle_output_M,
    b'C:': handle_output_C,
    b'L:': handle_output_L,
}
DEFAULT_OUTPUT = handle_output_default


