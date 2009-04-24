from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse, cgi

class GetHandler(BaseHTTPRequestHandler):
  # Defines if the server should parse for post variables.
  parse_post = True
  instance = None
  parent = None
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
        
    
    # Split that path data into the actual path, query-string, etc.
    path = urlparse.urlparse(self.path)
    # Get post variables
    variables = self.rfile.read(int(self.headers.get('content-length', 0)))
    # Parse get and post variables and store them in params object.
    parsed_post = urlparse.parse_qs(variables)
    parsed_get = urlparse.parse_qs(path.query)
    params = {
      'get': parsed_get,
      'post': parsed_post
    }
    
    status, data = self.instance.process(path.path, self.headers,
      params['get'], params['post'])
    
    self.send_response(status)
    self.end_headers()
    self.wfile.write(data)
    
    #print self.request
    
    request_parts = self.requestline.split(' ')
    #print request_parts
    return
class Server(object):
  server = None
  instance = None
  def __init__(self, host, port, instance, parse_for_post = True):
    server = HTTPServer(('localhost', 8080), GetHandler)
    self.instance = instance
    server.RequestHandlerClass.instance = instance
    server.RequestHandlerClass.parent = self
    if not parse_for_post:
      server.parse_post = False
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()