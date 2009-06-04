class Request(object):
  """
  # Dict of headers sent with the request from the client
  request_headers = {}
  # List of headers
  headers = []
  status = 200
  # Raw path (EG: "/test/abc/123")
  path = None
  # GET/POST variables
  get = {}
  post = {}
  # User agent of the client
  user_agent = ''
  # IP address of client
  ip_address = ''
  # Actual Constrictor instance
  instance = None
  # Instance of the server; used to grab host, port, etc.
  server_instance = None
  # Session class
  session = {}
  """
  def redirect(self, location, status = 302):
    self.headers.append('Location: ' + location.strip())
    self.status = status
    data = self.instance.config['Pages']['Redirect']
    data = data.replace('{path}', location)
    data = data.replace('{status}', str(status))
    return data
    