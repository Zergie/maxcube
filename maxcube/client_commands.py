# -*- coding: utf-8 -*-
from maxcube.message_fields import *

# == DONE ==
# OUTGOING_SEND = "s:";
# OUTGOING_QUIT = "q:";
# OUTGOING_GET_DEVICE_LIST = "l:";
# OUTGOING_GET_CONFIGURATION = "c:";

# == TODO ==
# OUTGOING_URL = "u:";
# OUTGOING_INTERVAL = "i:";
# OUTGOING_METADATA = "m:";
# OUTGOING_INCLUSION_MODE = "n:";
# OUTGOING_CANCEL_INCLUSION_MODE = "x:";
# OUTGOING_MORE_DATA = "g:";
# OUTGOING_ENCRYPTION = "e:";
# OUTGOING_DECRYPTION = "d:";
# OUTGOING_SET_CREDENTIALS = "B:";
# OUTGOING_GET_CREDENTIALS = "G:";
# OUTGOING_SET_REMOTEACCESS = "J:";
# OUTGOING_SET_USER_DATA = "P:";
# OUTGOING_GET_USER_DATA = "O:";
# OUTGOING_CHECK_PRODUCT_ACTIVATION = "V:";
# OUTGOING_ACTIVATE_PRODUCT = "W:";
# OUTGOING_SEND_DEVICE_CMD = "s:";
# OUTGOING_RESET = "a:";
# OUTGOING_RESET_ERROR = "r:";
# OUTGOING_DELETE_DEVICES = "t:";
# OUTGOING_SET_PUSHBUTTON_CONFIG = "w:";
# OUTGOING_SET_URL = "u:";
# OUTGOING_TIME_CONFIG = "v:";
# OUTGOING_NTP_SERVER = "f:";
# OUTGOING_SEND_WAKEUP = "z:";

class l_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'l:'),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)


class q_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'q:'),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)


class s_Message(MessageTyp):
   def __init__(self):
        self.fields = [ffixed('msg_type', b's:'),
                       fbase64(
                               ffixed('magic', [0x00, 0x04, 0x40, 0x00, 0x00, 0x00]),
                               ffield('rf_address' ,   3, bytes),
                               ffield('room_id'    ,   1, int),
                               ffield('temp'       ,   1, temp),
                               ffield('date_until' ,   2, datetime.date, True),
                               ffield('time_until' ,   1, datetime.time, True)),
                       ffixed('_end', b'\r\n') ]
        MessageTyp.__init__(self)


class c_Message(MessageTyp):
    def __init__(self):
        self.fields = [ffixed('msg_type', b'c:'),
                       ffield('rf_address', 6, str),
                       ffixed('_end', b'\r\n') ]    
        MessageTyp.__init__(self)

