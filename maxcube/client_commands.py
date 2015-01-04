# -*- coding: utf-8 -*-
from maxcube.message_fields import *

# == DONE ==
# OUTGOING_SEND = "s:"
# OUTGOING_QUIT = "q:"
# OUTGOING_GET_DEVICE_LIST = "l:"
# OUTGOING_GET_CONFIGURATION = "c:"

# == TODO ==
# OUTGOING_URL = "u:"
# OUTGOING_INTERVAL = "i:"
  # exmaple: 'n:??????????' + ',' + '????' + '\r\n'
  #            | interval   |     |  0x00  |
# OUTGOING_METADATA = "m:"
  # example: 'm:00,VgICAQZLw7xjaGUPw4ACCldvaG56aW1tZXIP2u0CAQ/DgExFUTExMzkwNTYMVGhlcm1vc3RhdCAxAQEP2u1MRVExMTM5NjIwDFRoZXJtb3N0YXQgMQIB\r\n'                                         -> base64('V\x02\x02\x01\x06K\xc3\xbcche\x0f\xc3\x80\x02\nWohnzimmer\x0f\xda\xed\x02\x01\x0f\xc3\x80LEQ1139056\x0cThermostat 1\x01\x01\x0f\xda\xedLEQ1139620\x0cThermostat 1\x02\x01')
  #          'm:00,VgICAQZLw7xjaGUPw4ACCldvaG56aW1tZXIP2u0DAQ/DgExFUTExMzkwNTYMVGhlcm1vc3RhdCAxAQEP2u1MRVExMTM5NjIwDFRoZXJtb3N0YXQgMQIBD8NzTEVRMTEzOTA2NAxUaGVybW9zdGF0IDICAQ==\r\n' -> base64('V\x02\x02\x01\x06K\xc3\xbcche\x0f\xc3\x80\x02\nWohnzimmer\x0f\xda\xed\x03\x01\x0f\xc3\x80LEQ1139056\x0cThermostat 1\x01\x01\x0f\xda\xedLEQ1139620\x0cThermostat 1\x02\x01\x0f\xc3sLEQ1139064\x0cThermostat 2\x02\x01')

# OUTGOING_INCLUSION_MODE = "n:" # FetchNewDevice
  # example: 'n:' +        '003c'      + '\r\n'
  #               | Timeout in seconds |
# OUTGOING_CANCEL_INCLUSION_MODE = "x:"
  # example: 'x:\r\n'
# OUTGOING_MORE_DATA = "g:"
# OUTGOING_ENCRYPTION = "e:"
# OUTGOING_DECRYPTION = "d:"
# OUTGOING_SET_CREDENTIALS = "B:"
# OUTGOING_GET_CREDENTIALS = "G:"
# OUTGOING_SET_REMOTEACCESS = "J:"
# OUTGOING_SET_USER_DATA = "P:"
# OUTGOING_GET_USER_DATA = "O:"
# OUTGOING_CHECK_PRODUCT_ACTIVATION = "V:"
# OUTGOING_ACTIVATE_PRODUCT = "W:"
# OUTGOING_SEND_DEVICE_CMD = "s:"
# OUTGOING_RESET = "a:"
  # example: 'a:\r\n'
# OUTGOING_RESET_ERROR = "r:"
# OUTGOING_DELETE_DEVICES = "t:"
# OUTGOING_SET_PUSHBUTTON_CONFIG = "w:"
# OUTGOING_SET_URL = "u:"
# OUTGOING_TIME_CONFIG = "v:"
  # example: 'v:Q0VUAAAKAAMAAA4QQ0VTVAADAAIAABwg\r\n' -> base64('CET\x00\x00' + '\n'  + '\x00'      + '\x03'      + '\x00'       + '\x00'       + '\x0e'      + '\x10' 
  #                                                           + 'CEST\x00'    + '\x03'+ '\x00'      + '\x02'      + '\x00'       + '\x00'       + '\x1c'      + ' ')
  #                                                      winter | name        | month | day of week | hour of day | offset >> 24 | offset >> 16 | offset >> 8 | offset |
  #                                                    + summer | name        | month | day of week | hour of day | offset >> 24 | offset >> 16 | offset >> 8 | offset |
  #          'v:Q0VUAAAKAAMAAA4QQ0VTVAADAAIAABwg,3\r\n' -> 3 is "ntpUTCSeconds"
# OUTGOING_NTP_SERVER = "f:"
  # example: 'f:\r\n'
  #          'f:NTP-Server1,NTP-Server2'
# OUTGOING_SEND_WAKEUP = "z:"
  # example: 'z:1e,G,01\r\n'

class l_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'l:'),
                       ffixed('_end'    , b'\r\n') ]
        MessageTyp.__init__(self)


class q_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'q:'),
                       ffixed('_end'    , b'\r\n') ]
        MessageTyp.__init__(self)


#class f_Message(MessageTyp):
#    def __init__(self):
#        self.fields = [ffixed('msg_type', b'f:'),
#                       ffield('url'     , ALL, str, True)
#                       ffixed('_end'    , b'\r\n') ]
#        MessageTyp.__init__(self)


class s_Message(MessageTyp):
   def __init__(self):
        self.fields = [ffixed('msg_type', b's:'),
                       fbase64(
                               ffixed('unused'     ,   b'\x00'),
                               ffield('group'      ,   1, int),
                               ffield('type'       ,   1, int),
                               ffixed('unused2'    ,   [0x00, 0x00, 0x00]),
                               ffield('rf_address' ,   3, bytes),
                               ffield('room_id'    ,   1, int),
                               fchoose('type',
                                      {
                                      0x00 : [], 
                                      0x01 : [],
                                      0x02 : [],
                                      0x03 : [],
                                      0x10 : [
                                      ffield('unknown10'  ,  14, bytes)],
                                      0x11 : [
                                      ffield('temperature_comfort'     ,   1, temp),          
                                      ffield('temperature_eco'         ,   1, temp),      
                                      ffield('temperature_setpoint_max',   1, temp),               
                                      ffield('temperature_setpoint_min',   1, temp),               
                                      ffield('temperature_offset'      ,   1, temp_offset),         
                                      ffield('temperature_window_open' ,   1, temp),
                                      ffield('duration_window_open'    ,   1, int)],
                                      0x12 : [],
                                      0x20 : [
                                      ffield('destination_rf_address',   3, bytes),
                                      ffield('destination_type'      ,   1, int)],
                                      0x21 : [],
                                      0x22 : [
                                      ffield('new_room_id',   1, int)],
                                      0x23 : [],
                                      0x30 : [],
                                      0x40 : [
                                      ffield('temp'       ,   1, temp),
                                      ffield('date_until' ,   2, datetime.date),
                                      ffield('time_until' ,   1, datetime.time)],
                                      0x41 : [],
                                      0x42 : [],
                                      0x43 : [],
                                      0x44 : [],
                                      0x45 : [],
                                      0x50 : [],
                                      0x60 : [],
                                     -0x80 : [],
                                     -0x81 : [],
                                     -0x82 : [],
                                     -0xF0 : [],
                                     -0xF1 : [],
                                     -0xFF : [],
                                      })),
                       ffixed('_end'    , b'\r\n')]
        MessageTyp.__init__(self)


class c_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type'  , b'c:'),
                       ffield('rf_address', 6, str),
                       ffixed('_end'      , b'\r\n') ]    
        MessageTyp.__init__(self)

