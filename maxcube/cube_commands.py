# -*- coding: utf-8 -*-
from maxcube.fields import *

import datetime

# == DONE ==
# INCOMING_HELLO = "H:"
# INCOMING_DEVICE_LIST = "L:"
# INCOMING_CONFIGURATION = "C:"
# INCOMING_METADATA = "M:"

# == TODO ==
# INCOMING_NTP_SERVER = "F:"
# INCOMING_NEW_DEVICE = "N:"
  # example: 'N:AQ/DgExFUTExMzkwNTag\r\n' -> base64(b'\x01\x0f\xc3\x80LEQ1139056\xa0')
  #                                                  | rf adress | ?? | serial | ?? |
  #          'N:\r\n'
  #          'N:AQ/Dc0xFUTExMzkwNjSg\r\n' -> base64(b'\x01\x0f\xc3sLEQ1139064\xa0')
  #          'N:AQ/a7UxFUTExMzk2MjCg\r\n' -> base64(b'\x01\x0f\xda\xedLEQ1139620\xa0')
# INCOMING_ACKNOWLEDGE = "A:"
  # example: 'A:\r\n'
# INCOMING_ENCRYPTION = "E:"
# INCOMING_DECRYPTION = "D:"
# INCOMING_SET_CREDENTIALS = "b:"
# INCOMING_GET_CREDENTIALS = "g:"
# INCOMING_SET_REMOTEACCESS = "j:"
# INCOMING_SET_USER_DATA = "p:"
# INCOMING_GET_USER_DATA = "o:"
# INCOMING_CHECK_PRODUCT_ACTIVATION = "v:"
# INCOMING_ACTIVATE_PRODUCT = "w:"
# INCOMING_SEND_DEVICE_CMD = "S:"
  # example: 'S:06,0,30\r\n'
  #          'S:03,0,2d\r\n' (response to 's:AAQQAAAAD9rtAgRASUxuQMtNIE0gTSBNIA==\r\n')
  #          'S:03,0,2a\r\n' (response to 's:AAQQAAAAD9rtAgZASUxuQMtNIE0gTSBNIA==\r\n')
  #          'S:04,0,2b\r\n' (response to 's:AAQQAAAAD9rtAgBASUxuQMtNIE0gTSBNIA==\r\n')

class H_Message(MessageTyp):
    def __init__(self):
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
        MessageTyp.__init__(self)


class C_Message(MessageTyp):
    def __init__(self):
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
                                            }))),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)


class M_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'M:')   ,
                       optional(fcsv(                                            
                            ffixed('index' , b'00'),                   
                            ffixed('count' , b'01'),
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
                                   ffield('unknown3', 1, int)
                                   ))),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)


class L_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'L:'),
                       optional(fbase64(
                               fmultiple('devices'                          , ALL,
                                      ffield('length'                       ,   1, int),
                                      ffield('rf_address'                   ,   3, bytes),
                                      ffield('unknown'                      ,   1, int),
                                      fflags(
                                            ['is_valid'      , 0b00010000, {0:True , 1:False}],
                                            ['error'         , 0b00001000, {0:False, 1:True}],
                                            ['is_answer'     , 0b00000100, {0:True , 1:False}],
                                            ['is_initialized', 0b00000010, {0:False, 1:True}]),
                                      fflags(
                                            ['battery_low'   , 0b10000000, {0:False, 1:True}],
                                            ['link_error'    , 0b01000000, {0:False, 1:True}],
                                            ['panel_locked'  , 0b00100000, {0:False, 1:True}],
                                            ['gateway_known' , 0b00010000, {0:False, 1:True}],
                                            ['dst active'    , 0b00001000, {0:False, 1:True}],
                                            ['mode'          , 0b00000011, {0:auto, 1:manual, 2:vacation, 3:boost}]),
                                      fchoose('length',
                                             {
                                             6  : [], 
                                             11 : [
                                              ffield('valve_position'      ,   1, percent),
                                              ffield('temperature_setpoint',   1, temp),
                                              ffield('date_until'          ,   2, datetime.date),
                                              ffield('time_until'          ,   1, datetime.time)]
                                              })))),
                       ffixed('_end', b'\r\n')]
        MessageTyp.__init__(self)


class S_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'S:'),
                       fcsv(
                           ffield('duty_cycle'       , ALL, int),
                           ffield('command_discarded', ALL, int),
                           ffield('free_memory_slots', ALL, int)
                        ),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)

