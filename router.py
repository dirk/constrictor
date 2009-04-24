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
  def get_parent_class(self):
    # Returns the class of the passed function, making it easy to instantiate
    # that controller class.
    try:
      return self.func.im_class
    except AttributeError:
      return None
  def match(self, url):
    # Use the compiled regex to match against the URL.
    match = self.route_rec.match(url)
    if match is None:
      # Did not match.
      return None
    else:
      # The URL matched, grab the params tuple.
      params = match.groups()
      return (self.get_parent_class(), self.func, params)