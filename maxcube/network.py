# -*- coding: utf-8 -*-

import socket


def read_raw_data(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(2)
    got = b''
    while True:
        try:
            got += s.recv(100000)
        except socket.timeout:
            break
    return got


def discover_cubes(limit=99):
    HelloMessage =  bytes([0x65, 0x51, 0x33, 0x4d, 0x61, 0x78, 0x2a, 0x00, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x2a, 0x49]);
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    sock.bind(('', 23272))
    sock.sendto(HelloMessage, ('224.0.0.1', 23272))

    while limit > 0:
        while True: 
            data, addr = sock.recvfrom(1024)
            
            if data[:8] == b'eQ3MaxAp':
                print (data[24:26])
                udp_answer = {
                    'serial' : data[8:18],
                    'unknown' : data[18:21],
                    'rf_address' : data[21:24],
                    'fw_version' : (data[24] >> 4)   * 1000 
                                 + (data[24] & 0x0F) * 100
                                 + (data[25] >> 4)   * 10
                                 + (data[25] & 0x0F)
                    }
                limit -= 1
                break
        sock.close()
        
        print(udp_answer)
        
        if udp_answer['fw_version'] < 109:
            yield addr[0], 80
        else:
            yield addr[0], 62910