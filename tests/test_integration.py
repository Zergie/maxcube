# -*- coding: utf-8 -*-
import os.path
import sys

from nose import tools
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, 'maxcube'))

from maxcube import objects

from test_parsing import RAW_DATA
from pprint import pprint

import threading
import socket

class DummyMaxCube(threading.Thread):
	def __init__(self, data):
		self.data  = data
		self.index = 0
		self.stop  = False
		threading.Thread.__init__(self, daemon=True)
	
	def run(self):
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind(('localhost', 9999))
		s.settimeout(2)
		s.listen(1)
		conn, addr = s.accept()

		try:
			while not self.stop:
				# send
				if not self.stop:
					data = self.data[self.index]
					self.index += 1
					for sent in data.split():
						sent += b'\r\n'
						conn.sendall(sent)
						print('sent:', sent)

				# recv
				got = b''
				while not self.stop:
					got = conn.recv(8192)
					if got.endswith('\r\n'):
						break
				print('got:', got)
		finally:
			conn.close()
			s.shutdown()




def test_integration():
	server = DummyMaxCube([RAW_DATA])
	server.start()

	cube = objects.MaxCube('localhost', 9999)
	cube.connect()

	server.stop = True

	# cube = objects.MaxCube('localhost', 123)
	# cube._setup(RAW_DATA)

	tools.assert_equal('0113', 		 cube.firmware_version)
	tools.assert_equal('JEQ0543545', cube.serial)
	tools.assert_equal('03f6c9', 	 cube.rf_address)

	tools.assert_equal(2, len(cube.rooms))
	tools.assert_equal(3, len(cube.devices))

	cube.devices[b'0b04be'].delete()
	pprint(cube)


if __name__ == '__main__':
	test_integration()
