# re will *definitely* be heavily used as this expands.
import re

class Route(object):
  # Regex to match the actual URL.
  route = None
  # The function (Normally from a controller.) used to process the request in
  # the case that the route matches.
  func = None
  # Simplest possible route, but allows for easy expansion later on instead of
  # using tuples, which would have limited the design and hampered expansion.
  def __init__(self, route, func):
    self.route = route;self.func = func
  def get_parent_class(self):
    # Returns the class of the passed function, making it easy to instantiate
    # that controller class.
    return self.func.im_class
  def match(self, url):
    # Assume we matched the URL.
    params = []
    return (self.get_parent_class(), self.func, params)