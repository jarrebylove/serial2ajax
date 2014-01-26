#!/usr/sbin/python2

import time

from jsonp_server import JSONPServer
from measuring_devices.demo_device import DemoDevice

HOST_NAME = 'localhost'
PORT_NUMBER = 9999
DEVICES = [
	DemoDevice(35.0, 1.0),
	DemoDevice(5.0, 0.1),
]

class Server(JSONPServer):
	def response(self, url):
		deviceNo = url.path.split('/')[1]
		if deviceNo.isdigit() and int(deviceNo) < len(DEVICES):
			return DEVICES[int(deviceNo)].getValue()
		else:
			return None

if __name__ == '__main__':
	server = Server(HOST_NAME, PORT_NUMBER)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		server.start()
	except KeyboardInterrupt:
		pass
	server.stop()
	for device in DEVICES:
		device.stop()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)
