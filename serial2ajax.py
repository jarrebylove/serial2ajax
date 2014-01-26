#!/usr/sbin/python2

import time
import BaseHTTPServer
import urlparse
import json

import thread

HOST_NAME = 'localhost'
PORT_NUMBER = 9999

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

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(s):
		s.send_response(200)
		s.send_header("Access-Control-Allow-Origin", "http://localhost/")
		s.send_header("Content-type", "application/json")
		s.end_headers()
		parsedPath = urlparse.urlparse(s.path)
		parsedQuery = urlparse.parse_qs(parsedPath.query)
		callback = parsedQuery['callback'][0]
		deviceNo = parsedPath.path.split('/')[1]
		if deviceNo.isdigit() and int(deviceNo) < len(devices):
			data = devices[int(deviceNo)].getValue()
		else:
			data = None
		data = json.dumps(data)
		s.wfile.write('{0}({1})'.format(callback, data))

devices = [
	DemoDevice(35.0, 1.0),
	DemoDevice(5.0, 0.1),
]

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	for device in devices:
		device.stop()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
