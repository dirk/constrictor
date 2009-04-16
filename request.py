class Request(object):
  # Stubbing out Request object.
  route = None
  controller = None
  
  def __init__(self, route, params={}):
    self.route = route
    self.controller = route.get_parent_class()
    self.method = route.func