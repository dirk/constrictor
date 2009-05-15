class Request(object):
  # Stubbing out Request object.
  
  # dict of headers
  request_headers = None
  headers = []
  path = None
  get = None
  post = None
  
  # Actual Constrictor instance
  instance = None
  
  session = {}
  """
  session = {
    'id': # md5 hash of random integer and system time.
    'user_agent': # Actual user-agent, combined with id for verification.
    'ip_address'
    'data': {}
  }
  """