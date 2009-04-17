from BaseHTTPServer import BaseHTTPRequestHandler
import urlparse

class GetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
      self.handle_request()
    def do_POST(self):
      self.handle_request()
    def do_PUT(self):
      self.handle_request()
    def do_DELETE(self):
      self.handle_request()
    def do_HEAD(self):
      self.handle_request()
    
    
    def handle_request(self):
        parsed_path = urlparse.urlparse(self.path)
        """message = '\n'.join([
                'CLIENT VALUES:',
                'client_address=%s (%s)' % (self.client_address,
                                            self.address_string()),
                'command=%s' % self.command,
                'path=%s' % self.path,
                'real path=%s' % parsed_path.path,
                'query=%s' % parsed_path.query,
                'request_version=%s' % self.request_version,
                '',
                'SERVER VALUES:',
                'server_version=%s' % self.server_version,
                'sys_version=%s' % self.sys_version,
                'protocol_version=%s' % self.protocol_version,
                '',
                ])"""
        self.send_response(200)
        self.end_headers()
        #self.wfile.write(message)
        variables = self.rfile.read(int(self.headers.get('content-length', 0)))
        request_parts = self.requestline.split(' ')
        print request_parts
        return

if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), GetHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()