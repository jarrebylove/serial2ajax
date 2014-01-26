import BaseHTTPServer
import urlparse
import json

class JSONPHandler(BaseHTTPServer.BaseHTTPRequestHandler):
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type', 'application/json')
		self.end_headers()
		url = urlparse.urlparse(self.path)
		query = urlparse.parse_qs(url.query)
		callback = query['callback'][0]
		data = self.response(url)
		data = json.dumps(data)
		self.wfile.write('%s(%s)'%(callback, data))
	
	def response(self, url):
		return None

class JSONPServer(BaseHTTPServer.HTTPServer):
	def __init__(self, host, port):
		JSONPHandler.response = self.response
		BaseHTTPServer.HTTPServer.__init__(self, (host, port), JSONPHandler)
	
	def start(self):
		self.serve_forever()
	
	def stop(self):
		self.server_close()
	
	def response(self, url):
		return None
