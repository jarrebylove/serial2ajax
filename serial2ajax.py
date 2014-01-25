#!/usr/sbin/python2

import time
import BaseHTTPServer
import urlparse
import json

HOST_NAME = '192.168.4.222'
PORT_NUMBER = 80

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Access-Control-Allow-Origin", "http://localhost/")
		s.send_header("Content-type", "application/json")
		s.end_headers()
	def do_GET(s):
		s.send_response(200)
		s.send_header("Access-Control-Allow-Origin", "http://localhost/")
		s.send_header("Content-type", "application/json")
		s.end_headers()
		parsed_path = urlparse.urlparse(s.path)
		parsed_query = urlparse.parse_qs(parsed_path.query)
		callback = parsed_query['callback'][0]
		data = [ { 'a':'A', 'b':(2, 4), 'c':3 } ]
		data = json.dumps(data)
		s.wfile.write('{0}({1})'.format(callback, data))

if __name__ == '__main__':
	server_class = BaseHTTPServer.HTTPServer
	httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
	print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER)
	try:
		httpd.serve_forever()
	except KeyboardInterrupt:
		pass
	httpd.server_close()
	print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)

