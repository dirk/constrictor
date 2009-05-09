class RequestResponse(object):
  headers = []
  data = []
class Request(object):
  # Stubbing out Request object.
  
  # dict of headers
  headers = None
  path = None
  get = None
  post = None
  
  # Actual Constrictor instance
  instance = None
  # Response instance
  response = RequestResponse()
  
  #def __init__(self, path, headers, get, post):
  #  self.path = path
  #  self.headers = headers
  #  self.get = get
  #  self.post = post