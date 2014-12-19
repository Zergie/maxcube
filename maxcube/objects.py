# -*- coding: utf-8 -*-

from maxcube import composing
from maxcube import network
from maxcube import parsing
from maxcube import output

class MaxCube(object):
	type_code = 0

	def __init__(self, host, port):
		self.host = host
		self.port = port

	def connect(self):
		raw_data = network.read_raw_data(self.host, self.port)
		self._setup(raw_data)

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
			self.devices[obj_device.serial] = obj_device 

			if obj_device.room_id:
				self.rooms[obj_device.room_id]._add_device(obj_device)

		# config for devices
		for config in configuration:
			if config['type'] != 0:
				self.devices[config['serial']]._add_configuration(config)



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

	def set_temp_permanent(self, temp):
		message = composing.compose_s(self.rf_address, self.room_id, temp, 1, None, None)
		print('-> ', message)

		raw_data = network.write_raw_data(self.cube.host, self.cube.port, message)
		self.cube._setup(raw_data)
		output.display(self.cube)
		#print('<- ', message)

	def set_temp_until(self, temp, date_until, time_until):
		message = composing.compose_s(self.rf_address, self.room_id, temp, 2, date_until, time_until)
		message = network.write_raw_data(self.cube.host, self.cube.port, message)
		

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

