# -*- coding: utf-8 -*-

class MaxCube(object):
	type_code = 0

	def __init__(self, address, serial, firmware_version):
		self.address = address
		self.serial = serial
		self.firmware_version = firmware_version
		self.rooms = {}
		self.devices = {}

	def add_room(self, room):
		self.rooms[room.id] = room

	def add_device(self, device):
		self.devices[device.serial] = device
		if device.room_id:
			self.rooms[device.room_id].add_device(device)


class Room(object):
	def __init__(self, id, address, name):
		self.id = id
		self.address = address
		self.name = name
		self.devices = []

	def add_device(self, device):
		self.devices.append(device)


class Device(object):
	def __init__(self, data):
		self.address = data['rf_address']
		self.serial  = data['serial']
		self.room_id = data['room_id']
		self.name 	 = data['name']

	def add_configuration(self, data):
		self.raw_data = data

	@classmethod
	def get_device_type(cls, type_code):
		return {c.type_code: c for c in cls.__subclasses__()}.get(type_code, cls)


class RadiatorThermostat(Device):
	type_code = 1

	def add_configuration(self, data):
		self.program = {
			'monday'	: data['program_mon'],
			'tuesday'	: data['program_tue'],
			'wednesday'	: data['program_wed'],
			'thursday'	: data['program_thu'],
			'friday'	: data['program_fri'],
			'saturday'	: data['program_sat'],
			'sunday'	: data['program_sun']
		}


class RadiatorThermostatPlus(Device):
	type_code = 2

	def add_configuration(self, data):
		RadiatorThermostat.add_configuration(self, data)

class WallThermostat(Device):
	type_code = 3
class ShutterContact(Device):
	type_code = 4
class EcoButton(Device):
	type_code = 5



def from_parsed_data(data):
	header = data['H'][0]
	meta = data['M'][0]
	configuration = data['C']

	cube = MaxCube(address=header['rf_address'], serial=header['serial'], firmware_version=header['firmware_version'])

	for room in meta['rooms'].values():
		cube.add_room(Room(id=room['id'], address=room['rf_address'], name=room['name']))

	for device in meta['devices']:
		klass = Device.get_device_type(device['type'])
		cube.add_device(klass(device))

	for config in configuration:
		if config['type'] != 0:
			cube.devices[config['serial']].add_configuration(config)

	return cube

