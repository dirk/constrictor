class Request(object):
  """
  # Dict of headers sent with the request from the client
  request_headers = {}
  # List of headers
  headers = []
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