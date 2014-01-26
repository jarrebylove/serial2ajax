import time
from measuring_device import MeasuringDevice

class DemoDevice(MeasuringDevice):
	def __init__(self, maxValue = 1.0, incrementValue = 0.1):
		MeasuringDevice.__init__(self)
		self.maxValue = maxValue
		self.incrementValue = incrementValue
		self.start()
	
	def update(self):
		if self.value < self.maxValue:
			self.value += self.incrementValue
		else:
			self.value = 0.0
		time.sleep(1)
