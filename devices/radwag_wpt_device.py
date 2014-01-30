import serial
import select
import math

from base_device import BaseDevice

class RadwagWPTDevice(BaseDevice):
	
	def __init__(self, port):
		BaseDevice.__init__(self)
		self.port = port
		self.start()
	
	def start(self):
		self.s = serial.Serial(self.port, 9600)
		self.s.nonblocking()
		BaseDevice.start(self)
	
	def update(self):
		readable, writable, exceptional = select.select([self.s], [], [])
		buff = readable[0].readline()
		if len(buff) == 21:
			value = buff[5:15].replace(' ', '')
			value = float(value)
			self.value = value
	
	def stop(self):
		BaseDevice.stop(self)
		self.s.close()
		self.buff = []
