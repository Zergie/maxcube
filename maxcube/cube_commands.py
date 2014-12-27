# -*- coding: utf-8 -*-
from maxcube.message_fields import *

import datetime

# INCOMING_HELLO = "H:";
# INCOMING_NTP_SERVER = "F:";
# done: INCOMING_DEVICE_LIST = "L:";
# done: INCOMING_CONFIGURATION = "C:";
# done: INCOMING_METADATA = "M:";
# INCOMING_NEW_DEVICE = "N:";
# INCOMING_ACKNOWLEDGE = "A:";
# INCOMING_ENCRYPTION = "E:";
# INCOMING_DECRYPTION = "D:";
# INCOMING_SET_CREDENTIALS = "b:";
# INCOMING_GET_CREDENTIALS = "g:";
# INCOMING_SET_REMOTEACCESS = "j:";
# INCOMING_SET_USER_DATA = "p:";
# INCOMING_GET_USER_DATA = "o:";
# INCOMING_CHECK_PRODUCT_ACTIVATION = "v:";
# INCOMING_ACTIVATE_PRODUCT = "w:";
# INCOMING_SEND_DEVICE_CMD = "S:";

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
                       fcsv(                                            
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
                                   )),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)


class L_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'L:'),
                       fbase64(
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
                                              }))),
                       ffixed('_end', b'\r\n')]
        MessageTyp.__init__(self)


class S_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'S:'),
                       fcsv(
                           ffield('unknown' , ALL, str),
                           ffield('unknown2', ALL, str),
                           ffield('unknown3', ALL, str)
                        ),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)

