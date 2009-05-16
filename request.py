class Request(object):
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
  # Dictionary to hold session variables, set by the Session system.
  session = {}
  """
  session = {
    'id': # md5 hash of random integer and system time.
    'user_agent': # Actual user-agent, combined with id for verification.
    'ip_address'
    'data': {}
  }
  """