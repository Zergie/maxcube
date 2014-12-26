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
                                            ffield('unknown'                 ,  66, bytes),
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
                                            ffield('program'                 , 182, weeklyprogram)],
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
                                            ffield('program'                 , 182, weeklyprogram)],
                                           3 : [
                                            ffield('temperature_comfort'     ,   1, temp),         
                                            ffield('temperature_eco'         ,   1, temp),     
                                            ffield('temperature_setpoint_max',   1, temp),              
                                            ffield('temperature_setpoint_min',   1, temp),              
                                            ffield('program'                 , 182, weeklyprogram)],
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
                                   fmultiple('rooms'             ,  VL,
                                             ffield('id'         ,   1, int), 
                                             ffield('name'       ,  VL, str), 
                                             ffield('rf_address' ,   3, bytes)
                                            ),
                                   fmultiple('devices'           , VL,
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
                       fbase64(
                            fmultiple('devices'                             , ALL,
                                      ffield('length'                       ,   1, int),
                                      fchoose('length',
                                              {
                                              6 : [
                                               ffield('rf_address'          ,   3, bytes),
                                               ffield('unknown'             ,   1, int),
                                               ffield('flags_1'             ,   1, int),
                                               ffield('flags_2'             ,   1, int)],
                                              11 : [
                                               ffield('rf_address'          ,   3, bytes),
                                               ffield('unknown'             ,   1, int),
                                               ffield('flags_1'             ,   1, int),
                                               ffield('flags_2'             ,   1, int),
                                               ffield('valve_position'      ,   1, percent),
                                               ffield('temperature_setpoint',   1, temp),
                                               ffield('date_until'          ,   2, datetime.date),
                                               ffield('time_until'          ,   1, datetime.time)]
                                               })
                                      )
                              ),
                       ffixed('_end', '\r\n') ]
        MessageTyp.__init__(self, raw_bytes)




class l_Message(MessageTyp):
    def __init__(self, raw_bytes):
        self.fields = [ffixed('msg_type', b'l:')   ,
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
    cls = None

    for c in MessageTyp.__subclasses__():
        if c.__name__.startswith(msg_type):
            cls = c
            break

    if cls != None:
        message = c(line)
        return message
    else:
        return None
