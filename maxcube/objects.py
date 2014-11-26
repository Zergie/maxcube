# -*- coding: utf-8 -*-

class MaxCube(object):
	type_code = 0

	def __init__(self, address, serial, firmware_version):
		self.address = address
		self.serial = serial
		self.firmware_version = firmware_version
		self.rooms = {}
		self.devices = []

	def add_room(self, room):
		self.rooms[room.id] = room

	def add_device(self, device):
		self.devices.append(device)
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
	def __init__(self, address, serial, room_id, name):
		self.address = address
		self.serial = serial
		self.room_id = room_id
		self.name = name

	@classmethod
	def get_device_type(cls, type_code):
		return {c.type_code: c for c in cls.__subclasses__()}.get(type_code, cls)

	@classmethod
	def from_dict(cls, data):
		return cls(address=data['rf_address'], serial=data['serial'], room_id=data['room_id'], name=data['name'])

class RadiatorThermostat(object):
	type_code = 1
class RadiatorThermostatPlus(object):
	type_code = 2
class WallThermostat(object):
	type_code = 3
class ShutterContact(object):
	type_code = 4
class EcoButton(object):
	type_code = 5



def from_parsed_data(data):
	header = data['H'][0]
	meta = data['M'][0]
	cube = MaxCube(address=header['rf_address'], serial=header['serial'], firmware_version=header['firmware_version'])
	for room in meta['rooms'].values():
		cube.add_room(Room(id=room['id'], address=room['rf_address'], name=room['name']))
	for device in meta['devices']:
		klass = Device.get_device_type(device['type'])
		cube.add_device(klass.from_dict(device))
	return cube

