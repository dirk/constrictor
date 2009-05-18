from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse, cgi
# Used for headers
import time

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
  def log_request(self, log): pass
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
        
    
    """
    # TODO: Improve request handling system.
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
    """
    from constrictor.request import Request
    
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
    # Initialize Request class
    request = Request()
    # Assign basic server variables
    request.path = path.path
    request.instance = self.instance
    request.server_instance = self
    request.headers = []
    request.request_headers = dict(self.headers)
    request.get = params['get']
    request.post = params['post']
    request.user_agent = self.headers.get('user-agent')
    request.ip_address = self.client_address[0]
    # Actually process it, the Request will return a status code (EG: 200)
    # and the actual return content.
    status, data = self.instance.process(request)
    # Grab the list of headers from the request object.
    headers = request.headers
    # Send the status code
    self.send_response(status)
    # Iterate through headers and send them in the response.
    for header in headers:
      if type(header) is tuple or type(header) is list:
        # First item is the keyword, second is the value.
        self.send_header(header[0], header[1])
      elif type(header) is dict:
        self.send_header(header['keyword'], header['value'])
      elif type(header) is str:
        # Just a plain string (EG: 'Content-Type: image/png'), split it into
        # a two item list and pass that to send_header.
        self.send_header(*header.split(': ', 1))
      else:
        raise Exception, 'Header is not tuple, list, or dict'
    # End header sending and output the data.
    self.end_headers()
    self.wfile.write(data)
    
    del(request)
    return
class Server(object):
  server = None
  instance = None
  def __init__(self, host, port, instance, parse_for_post = True):
    server = HTTPServer((host, port), GetHandler)
    self.instance = instance
    server.RequestHandlerClass.instance = instance
    # FIXME: Host and domain will be difference for a production environment
    server.RequestHandlerClass.host = host
    server.RequestHandlerClass.domain = host
    server.RequestHandlerClass.parent = self
    if not parse_for_post:
      server.parse_post = False
    print 'Starting server, use <Ctrl-C> to stop.'
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      print '\nServer shutdown.'