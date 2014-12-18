# -*- coding: utf-8 -*-

import base64
import datetime

def compose_s(rf_adress, room_id, temp, mode, date_until, time_until):
	# modes:
	# 0 = Auto weekprog (no temp is needed, just make the whole byte 00)
	# 1 = Permanent
	# 2 = Temporarily

	message = bytes(compile_s(rf_adress, room_id, temp, mode, date_until, time_until))

	ret  = b's:' 
	for i in base64.encodebytes(message):
		if i != 0xA: ret += bytes([i])
	ret += b'\r\n'

	return ret 


def compile_s(rf_adress, room_id, temp, mode, date_until, time_until):
	temp_pair = [(temp * 2) + (mode<<6)]

	if date_until == None:
		date_encoded = []
	else:
		date_encoded  = (date_until.year - 2000)
		date_encoded += ((date_until.month & 0x01) << 7) 
		date_encoded += ((date_until.month & 0x0E) << 12) 
		date_encoded += (date_until.day << 8)

		date_encoded  = [(date_encoded & 0xFF00) >> 8, (date_encoded & 0x00FF)]

	if time_until == None:
		time_encoded = []
	else:
		time_encoded = [int((float(time_until.hour) + float(time_until.minute / 60)) * 2)]

	message  = [0x00, 0x04, 0x40, 0x00, 0x00, 0x00]
	message += rf_adress
	message += [room_id]
	message += temp_pair
	message += date_encoded
	message += time_encoded

	return message



print('-- Test 1 --')
print(b's:AARAAAAAAP4wAaiLix8=\r\n')
print(compose_s(bytes([0x00, 0xfe, 0x30]), 1, 20, 2, datetime.date(2011, 9, 11), datetime.time(15, 30)))


print('-- Test 2 --')
print([hex(i) for i in [0x00, 0x04, 0x40, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x30, 0x01, 0x00]])
print([hex(i) for i in compile_s([0x00, 0xfe, 0x30], 1, 0, 0, None, None)])

print(b's:AARAAAAAAP4wAQA=\r\n')
print(compose_s(bytes([0x00, 0xfe, 0x30]), 1, 0, 0, None, None))


print('-- Test 3 --')
print([hex(i) for i in [0x00, 0x04, 0x40, 0x00, 0x00, 0x00, 0x00, 0xFE, 0x30, 0x01, 0x6C]])
print([hex(i) for i in compile_s(bytes([0x00, 0xfe, 0x30]), 1, 22, 2, None, None)])
print([hex(i) for i in compile_s(bytes([0x00, 0xfe, 0x30]), 1, 22, 1, None, None)])
print([hex(i) for i in compile_s(bytes([0x00, 0xfe, 0x30]), 1, 22, 0, None, None)])
