import serial
import select
import math

from base_device import BaseDevice

class UT70BDevice(BaseDevice):
	NAME = 0
	UNIT = 1
	FACTOR = 2
	PREFIX = 3
	
	tab = {
		'1': [
			'Diode test',
			['V',],
			[[-3,],],
			[[0,],],
		],
		'2': [
			'Frequency',
			['Hz', 'RPM',] ,
			[[0, 1, 2, 3, 4, 5], [-2, -1, 0, 1, 2, 3],],
			[[3, 3, 3, 6, 6, 6], [3, 3, 6, 6, 6, 6],],
		],
		'3': [
			'Resistance',
			['Ohm',],
			[[-1, 0, 1, 2, 3, 4,],],
			[[0, 3, 3, 3, 6, 6,],],
		],
		'4': [
			'Temperature',
			['F', 'C',],
			[[0,], [0,],],
			[[0,], [0,],],
		],
		'5': [
			'Continuity',
			['Ohm',],
			[[-1,],],
			[[0,],],
		],
		'6': [
			'Capacity',	
			['F',],	
			[[-12, -11, -10, -9, -8, -7, -6, -5,],],
			[[-9, -9, -9, -6, -6, -6, -3, -3,],],
		],
		'9': [
			'Current', #mA
			['A',],	
			[[-5, -4,],],
			[[-3, -3,],],
		],
		';': [
			'Voltage',
			['V',],	
			[[-4, -3, -2, -1, 0,],],
			[[-3, 0, 0, 0, 0,],],
		],
		'=': [
			'Current', #uA
			['A',],
			[[-7, -6,],],
			[[-6, -6,],],
		],
		'?': [
			'Current', #A
			['A',],
			[[-2,],],
			[[0,],],
		],
	}
	
	unitsPrefix = {
		-12:	'p',
		-9:		'n',
		-6:		'u',
		-3:		'm',
		0:		'',
		3:		'k',
		6:		'M',
		9:		'G',
		12:		'T',
	}
	
	def __init__(self, port):
		BaseDevice.__init__(self)
		self.port = port
		self.buff = []
		self.start()
	
	def start(self):
		self.s = serial.Serial(self.port, 2400)
		self.s.setDTR(True)
		self.s.setRTS(False)
		self.s.nonblocking()
		BaseDevice.start(self)
	
	def update(self):
		readable, writable, exceptional = select.select([self.s], [], [])
		self.buff.append(chr(ord(readable[0].read()) & 0b01111111))
		if len(self.buff) == 11 and self.buff[-2] == '\r' and self.buff[-1] == '\n':
			measurement = self.tab[self.buff[5]][self.NAME]
			acdc = ['', ' AC', ' DC', ''][(ord(self.buff[8]) & 0b00001100) >> 2]
			measurement += acdc
			altUnit = bool(ord(self.buff[6]) & 0b00001000)
			value = float(''.join(self.buff[1:5]))
			sing = [1.0, -1.0][bool(ord(self.buff[6]) & 0b00000100)]
			factorIndex = self.tab[self.buff[5]][self.FACTOR][altUnit][int(self.buff[0])]
			factor = float(10 ** factorIndex)
			value *= sing * factor
			prefixIndex = self.tab[self.buff[5]][self.PREFIX][altUnit][int(self.buff[0])]
			value /= float(10 ** prefixIndex)
			prefix = self.unitsPrefix[prefixIndex]
			unit = self.tab[self.buff[5]][self.UNIT][altUnit]
			unit = prefix + unit
			over = ['', 'Overload'][bool(ord(self.buff[6]) & 0b00000001)]
			result = '{:s} {:.{prec}f} {:s} {:s}'.format(measurement, value, unit, over, prec = abs(factorIndex - prefixIndex))
			#print(result)
			self.value = value
			self.buff = []
		elif len(self.buff) > 11:
			self.buff = []
	
	def stop(self):
		BaseDevice.stop(self)
		self.s.close()
		self.buff = []
