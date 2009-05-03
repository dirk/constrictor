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
  def process(self, flags):
    method, params = self._match_route(self.path)
    # See if it is an instance method of a class, and if it is, get that class.
    try:
      klass = method.im_class
    except AttributeError: klass = None
    if klass:
      klass_instance = klass()
      bound_method = klass_instance.__getattribute__(method.__name__)
      status, data = bound_method(self, params)
      #print klass_instance.__dict__[method.__name__].__call__(self, params)
      #print klass.__dict__[method.__name__].__call__(klass, self, params)
    else:
      status, data = method(self, params)
    print status
    print data
    return (0,0,0)
  def _match_route(self, path):
    # Iterate through routes and find which matches
    for route in self.instance.routes:
      route_result = route.match(path)
      if route_result:
        # If it does match, return the route.
        return route_result
    # It didn't match, then the pointer will end up here and raise the
    # route not matched Exception.
    raise Exception(404, 'Route not matched')