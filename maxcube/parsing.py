# -*- coding: utf-8 -*-
from maxcube.message_fields import *

import datetime


class H_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [ffixed('msg_type', b'H:')   ,
                       fcsv(
                            ffield('serial'            , ALL, str),
                            ffield('rf_address'        , ALL, str),
                            ffield('firmware_version'  , ALL, str),
                            ffield('unknown'           , ALL, str),
                            ffield('http_connection_id', ALL, str),
                            ffield('duty_cycle'        , ALL, str),
                            ffield('free_memory_slots' , ALL, str),
                            ffield('cube_date'         , ALL, datetime.date),
                            ffield('cube_time'         , ALL, datetime.time),
                            ffield('clock_set'         , ALL, str),
                            ffield('unknown2'          , ALL, str)
                            ),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self, raw_bytes)



class C_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [ffixed('msg_type', b'C:')   ,
                       fcsv(
                            ffield('rf_address_2', ALL, str),
                            fbase64(
                                    ffield('data_len'        ,   1, int),
                                    ffield('rf_address'      ,   3, bytes),
                                    ffield('type'            ,   1, int),
                                    ffield('room_id'         ,   1, int),
                                    ffield('firmware_version',   1, int),
                                    ffield('test_result'     ,   1, int),
                                    ffield('serial'          ,  10, str),
                                    fchoose('type',
                                           {
                                           0 : [
                                            ffield('portal_enabled'          ,   1, int),
                                            ffield('unknown'                 ,  65, bytes),
                                            ffield('portal_url'              ,  T0, str)],
                                           1 : [
                                            ffield('temperature_comfort'     ,   1, temp),          
                                            ffield('temperature_eco'         ,   1, temp),      
                                            ffield('temperature_setpoint_max',   1, temp),               
                                            ffield('temperature_setpoint_min',   1, temp),               
                                            ffield('temperature_offset'      ,   1, temp),         
                                            ffield('temperature_window_open' ,   1, temp),              
                                            ffield('duration_window_open'    ,   1, int),           
                                            ffield('duration_boost'          ,   1, int),     
                                            ffield('decalcification'         ,   1, int),      
                                            ffield('valve_maximum'           ,   1, percent),    
                                            ffield('valve_offset'            ,   1, percent),   
                                            ffield('program_sat'             ,  26, bytes),   
                                            ffield('program_sun'             ,  26, bytes),   
                                            ffield('program_mon'             ,  26, bytes),   
                                            ffield('program_tue'             ,  26, bytes),   
                                            ffield('program_wed'             ,  26, bytes),   
                                            ffield('program_thu'             ,  26, bytes),   
                                            ffield('program_fri'             ,  26, bytes)],
                                           2 : [
                                            ffield('temperature_comfort'     ,   1, temp),          
                                            ffield('temperature_eco'         ,   1, temp),      
                                            ffield('temperature_setpoint_max',   1, temp),               
                                            ffield('temperature_setpoint_min',   1, temp),               
                                            ffield('temperature_offset'      ,   1, temp_offset),         
                                            ffield('temperature_window_open' ,   1, temp),              
                                            ffield('duration_window_open'    ,   1, int),           
                                            ffield('duration_boost'          ,   1, int),     
                                            ffield('decalcification'         ,   1, int),      
                                            ffield('valve_maximum'           ,   1, percent),    
                                            ffield('valve_offset'            ,   1, percent),   
                                            ffield('program_sat'             ,  26, bytes),   
                                            ffield('program_sun'             ,  26, bytes),   
                                            ffield('program_mon'             ,  26, bytes),   
                                            ffield('program_tue'             ,  26, bytes),   
                                            ffield('program_wed'             ,  26, bytes),   
                                            ffield('program_thu'             ,  26, bytes),   
                                            ffield('program_fri'             ,  26, bytes)],
                                           3 : [
                                            ffield('temperature_comfort'     ,   1, temp),         
                                            ffield('temperature_eco'         ,   1, temp),     
                                            ffield('temperature_setpoint_max',   1, temp),              
                                            ffield('temperature_setpoint_min',   1, temp),              
                                            ffield('program_sat'             ,  26, bytes),   
                                            ffield('program_sun'             ,  26, bytes),   
                                            ffield('program_mon'             ,  26, bytes),   
                                            ffield('program_tue'             ,  26, bytes),   
                                            ffield('program_wed'             ,  26, bytes),   
                                            ffield('program_thu'             ,  26, bytes),   
                                            ffield('program_fri'             ,  26, bytes)],
                                           4 : [],
                                           5 : []
                                            }),
                                   ),
                           ),
                       ffixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)



class M_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [ffixed('msg_type', b'M:')   ,
                       fcsv(                                            
                            ffixed('unknown' , '00'),                   
                            ffixed('unknown2', '01'),
                            fbase64(                                    
                                   ffixed('magicbyte', 0x56          ), 
                                   ffixed('version'  , 0x02          ),
                                   fmultiple('rooms'                  ,
                                             ffield('id'         ,   1, int), 
                                             ffield('name'       ,  VL, str), 
                                             ffield('rf_address' ,   3, bytes)
                                            ),
                                   fmultiple('devices'                ,
                                             ffield('type'       ,   1, int),
                                             ffield('rf_address' ,   3, bytes),
                                             ffield('serial'     ,  10, str),
                                             ffield('name'       ,  VL, str),
                                             ffield('room_id'    ,   1, int)
                                            ),
                                   ffield('unknown3', ALL, int)
                                   )
                            ),
                       ffixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)



class L_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [ffixed('msg_type', b'L:')   ,
                       fcsv(
                           ),
                       ffixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)



#class s_Message(MessageTyp):
#    def __init__(self):
#        self.fields = {'msg_type'            : ffixed('s:')    ,
#                        fbase64('magic'     ,  ffixed([0x00, 0x04, 0x40, 0x00, 0x00, 0x00]) ,
#                                'rf_address',  pHex()          ,
#                                'room_id'   ,  pHex()          ,
#                                'temp_pair' ,  pTempPair()     ,
#                                'date'      ,  pHexDate(0, 1)  ,
#                                'time'      ,  pHexTime(0, 1)) ,
#                       ''                   :  ffixed('\r\n')  }
#                      }

def start(raw_data):
    ret = []
    for line in raw_data.split(b'\r\n'):
        if len(line) > 0:
            ret.append(handle_output(line + b'\r\n'))
    return ret

def handle_output(line):
    #print('handle_output=', line)
    msg_type = chr(line[0]) + '_'
    
    for c in MessageTyp.__subclasses__():
        if c.__name__.startswith(msg_type):
            break

    message = c(line)
    return message

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


