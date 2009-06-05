import re
from controller import Controller

class Route(object):
  # Regex to match the actual URL.
  route = None
  # Stores the compiled version of the route. rec = Regex Compiled
  route_rec = None
  # The function (Normally from a controller.) used to process the request in
  # the case that the route matches.
  func = None
  # Simplest possible route, but allows for easy expansion later on instead of
  # using tuples, which would have limited the design and hampered expansion.
  def __init__(self, route, func):
    self.route = route
    self.route_rec = re.compile(route)
    self.func = func
  def match(self, url):
    # Use the compiled regex to match against the URL.
    match = self.route_rec.match(url)
    if match is None:
      # Did not match.
      return None
    else:
      # The URL matched, grab the params tuple.
      params = match.groups()
      return (self.func, params)
class Controller_Route(object):
  """
  Takes a controller and allows for easy auto-routing to it's methods in the
  style "/controller/method/params".
  """
  def __init__(self, controller, controller_name = False):
    self.controller = controller
    if not controller_name: controller_name = controller.__name__.lower()
    self.route_rec = re.compile(r'^/%s/?([0-9A-z-_]+)?/?([^/]+)?/?$' % controller_name)
  def match(self, url):
    match = self.route_rec.match(url)
    if not match is None:
      groups = match.groups()
      method_name = groups[0];params = groups[1]
      if method_name is None: method_name = 'index'
      try:
        method = type.__getattribute__(self.controller, method_name)
        return (method, params)
      except AttributeError: return None
    else: return None