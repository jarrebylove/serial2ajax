import thread

class MeasuringDevice():
	def __init__(self):
		self.running = False
		self.value = 0.0
	
	def start(self):
		self.running = True
		thread.start_new_thread(self.run, ())
	
	def stop(self):
		self.running = False
	
	def run(self):
		while(self.running):
			self.update()
	
	def update(self):
		self.value = 0.0
		time.sleep(1)
	
	def getValue(self):
		return '%.3f'%(self.value)
