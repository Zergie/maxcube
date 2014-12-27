# -*- coding: utf-8 -*-

from maxcube import network
from maxcube import parsing
from maxcube import output
from maxcube.cube_commands import *

import socket

class MaxCube(object):
	type_code = 0

	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = None

		self.rf_address       = None
		self.serial           = None
		self.firmware_version = None

		self.devices              = {}
		self.rooms                = {}
		self.radiator_thermostats = []
		self.wall_thermostats     = []
		self.shutter_contacts     = []
		self.eco_buttons          = []

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
		for msg in parsing.start(raw_data):
			if isinstance(msg, H_Message):
				self.rf_address       = msg.rf_address
				self.serial           = msg.serial
				self.firmware_version = msg.firmware_version

			elif isinstance(msg, M_Message):
				for room in msg.rooms:
					obj_room = Room(self, room.id, room.rf_address, room.name)
					self.rooms[room.id] = obj_room

				for device in msg.devices:
					if device.type == 1:
						klass  = RadiatorThermostat
						llist  = self.radiator_thermostats
					elif device.type == 2:
						klass  = RadiatorThermostatPlus
						llist  = self.radiator_thermostats
					elif device.type == 3:
						klass  = WallThermostat
						llist  = self.wall_thermostats
					elif device.type == 4:
						klass  = ShutterContact
						llist  = self.shutter_contacts
					elif device.type == 5:
						klass  = EcoButton
						llist  = self.eco_buttons
					else:
						klass  = None
						llist  = None

					obj_device = klass(self, device)
					llist.append(obj_device)
					self.devices[obj_device.rf_address] = obj_device 

			elif isinstance(msg, L_Message):
				pass

			elif isinstance(msg, C_Message):
				if msg.type != 0:
					self.devices[msg.rf_address]._add_configuration(msg)


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
		self.rf_address = data.rf_address
		self.serial     = data.serial
		self.room_id    = data.room_id
		self.name 	    = data.name

	def _add_configuration(self, data):
		self.raw_data = data

	def status(self):
		status = self.cube.status()
		return status[self.rf_address]


class RadiatorThermostat(Device):
	type_code = 1

	def _add_configuration(self, config):
		self.program = config.program

	def set_temp(self, temp):
		message = b'l:'
		
		print('-> ', message)
		self.cube.sock.send(message)

		print('<- ', self.cube.sock.recv(1024))

	def set_temp_until(self, temp, date_until, time_until):
		pass
		
	def set_temp_auto(self):
		pass



class RadiatorThermostatPlus(RadiatorThermostat):
	type_code = 2
class WallThermostat(Device):
	type_code = 3
class ShutterContact(Device):
	type_code = 4
class EcoButton(Device):
	type_code = 5

