from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse, cgi
# Used for headers
import time

from constrictor.request import Request

class GetHandler(BaseHTTPRequestHandler):
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
  def log_request(self, status):
    # Damn errors takin' up mah LOC's.
    try:
      special = self.special
    except AttributeError: special = False
    if status == 200 and not special:
      # Make sure it's a 200 status (not 404) and that it's not a "special"
      # request (EG: favicon).
      log = self.client_address[0] + ': "' + self.path + '" '
      if self.response['core']['controller'] is None:
        controller = 'Default'
      else: controller = self.response['core']['controller'].__name__
      print log + '> ' + controller + '.' + self.response['core']['method'].__name__
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
    # TODO: Make this less h4x
    for key in parsed_post:
      if type(parsed_post[key]) is list:
        parsed_post[key] = parsed_post[key][0]
    for key in parsed_get:
      if type(parsed_get[key]) is list:
        parsed_get[key] = parsed_get[key][0]
    params = {
      'get': parsed_get,
      'post': parsed_post
    }
    # Initialize Request class and assign variables for use by the core,
    # controllers, plugins, etc.
    request = Request()
    request.path = path.path
    request.instance = self.instance;request.server_instance = self
    request.status = 200
    # Holds list of headers that will be built and eventually returned to
    # the client.
    request.headers = []
    request.request_headers = dict(self.headers)
    # GET and POST params.
    request.get = params['get'];request.post = params['post']
    # Used mainly by the Session system.
    request.user_agent = self.headers.get('user-agent')
    request.ip_address = self.client_address[0]
    # Actually process it, the Request will return a status code (EG: 200)
    # and the actual return content, plus a dict of debugging information.
    if request.path == '/favicon.ico':
      # A favicon is "special"!
      self.special = True
      data = self.instance.config['Favicon']['Data']
      request.headers.append((
        'Content-type',
        self.instance.config['Favicon']['Content-type']))
    else:
      data, debug = self.instance.process(request)
      if debug == 'Special':
        self.special = True
      else:
        # Set up some info. for the log_request() that gets called when
        # send_response() is called.
        self.response = {
          'core': debug
        }
    self.send_response(request.status) # Send the status code
    # Iterate through headers and send them in the response.
    for header in request.headers:
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
    del(request) # Yayzorz for garbage collection!
class Server(object):
  server = None
  instance = None
  def __init__(self, host, port, instance):
    server = HTTPServer((host, port), GetHandler)
    self.instance = instance
    server.RequestHandlerClass.instance = instance
    # FIXME: Host and domain will be different for a production environment
    server.RequestHandlerClass.host = host
    server.RequestHandlerClass.domain = host
    server.RequestHandlerClass.parent = self
    print 'Starting server, use <Ctrl-C> to stop.'
    try:
      server.serve_forever()
    except KeyboardInterrupt:
      print '\nServer shutdown.'