class Request(object):
  # Stubbing out Request object.
  def __init__(self, path, headers, get, post):
    self.path = path
    self.headers = headers
    self.get = get
    self.post = post