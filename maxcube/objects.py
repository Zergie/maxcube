# -*- coding: utf-8 -*-

from maxcube import composing
from maxcube import network
from maxcube import parsing
from maxcube import output

import socket

class MaxCube(object):
	type_code = 0

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = None

	def connect(self):
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((self.host, self.port))
		
		raw_data = b''
		while 1:
			buf = self.sock.recv(8192)
			raw_data += buf
			if buf[0:2] == b'L:': break
			
		self._setup(raw_data)

	def close(self):
		self.sock.close()

	def status(self):
		self.sock.send(b'l:\r\n')
		raw_data = self.sock.recv(8192)
		return parsing.handle_output(raw_data)[1]

	def _setup(self, raw_data):
		data          = parsing.start(raw_data)
		header        = data['H'][0]
		meta          = data['M'][0]
		configuration = data['C']

		self.rf_address       = header['rf_address']
		self.serial           = header['serial']
		self.firmware_version = header['firmware_version']	

		self.devices              = {}
		self.rooms                = {}
		self.radiator_thermostats = []
		self.wall_thermostats     = []
		self.shutter_contacts     = []
		self.eco_buttons          = []

		# rooms
		for room in meta['rooms'].values():
			obj_room = Room(self, room['id'], room['rf_address'], room['name'])
			self.rooms[room['id']] = obj_room

		# devices
		for device in meta['devices']:
			if device['type'] == 1:
				klass = RadiatorThermostat
				llist  = self.radiator_thermostats
			elif device['type'] == 2:
				klass = RadiatorThermostatPlus
				llist  = self.radiator_thermostats
			elif device['type'] == 3:
				klass = WallThermostat
				llist  = self.wall_thermostats
			elif device['type'] == 4:
				klass = ShutterContact
				llist  = self.shutter_contacts
			elif device['type'] == 5:
				klass = EcoButton
				llist  = self.eco_buttons
			else:
				klass = None
				llist  = None

			obj_device                      = klass(self, device)
			llist.append(obj_device)
			self.devices[obj_device.rf_address] = obj_device 

			if obj_device.room_id:
				self.rooms[obj_device.room_id]._add_device(obj_device)

		# config for devices
		for config in configuration:
			if config['type'] != 0:
				self.devices[config['rf_address']]._add_configuration(config)



class Room(object):
	def __init__(self, cube, id, rf_address, name):
		self.cube       = cube
		self.id         = id
		self.rf_address = rf_address
		self.name       = name
		self.devices    = []

	def _add_device(self, device):
		self.devices.append(device)



class Device(object):
	def __init__(self, cube, data):
		self.cube       = cube
		self.rf_address = data['rf_address']
		self.serial     = data['serial']
		self.room_id    = data['room_id']
		self.name 	    = data['name']

	def _add_configuration(self, data):
		self.raw_data = data

	def status(self):
		status = self.cube.status()
		return status[self.rf_address]


class RadiatorThermostat(Device):
	type_code = 1

	def _add_configuration(self, config):
		self.program = {
			'monday'	: config['program_mon'],
			'tuesday'	: config['program_tue'],
			'wednesday'	: config['program_wed'],
			'thursday'	: config['program_thu'],
			'friday'	: config['program_fri'],
			'saturday'	: config['program_sat'],
			'sunday'	: config['program_sun']
		}

	def set_temp(self, temp):
		message = composing.compose_s(self.rf_address, self.room_id, temp, 0, None, None)
		
		print('-> ', message)
		self.cube.sock.send(message)

		print('<- ', self.cube.sock.recv(1024))

	def set_temp_until(self, temp, date_until, time_until):
		message = composing.compose_s(self.rf_address, self.room_id, temp, 2, date_until, time_until)
		print(message)
		
	def set_temp_auto(self):
		message = composing.compose_s(self.rf_address, self.room_id, 0, 0, None, None)
		print(message)



class RadiatorThermostatPlus(RadiatorThermostat):
	type_code = 2
class WallThermostat(Device):
	type_code = 3
class ShutterContact(Device):
	type_code = 4
class EcoButton(Device):
	type_code = 5

