import os, sys

from controller import Expose, Filter

# Core class.
# TODO: Improve upon core class.
# TODO: Start working on full definition of request handling system.
class Constrictor(object):
  # Importing version number and representation function.
  import __init__ as version
  # Sub-classing:
  # - Controller
  from controller import Controller
  # - Route class for routing system
  from router import Route
  # - Request class used in routing and processing system.
  from request import Request
  
  routes = []
  # Initialization
  def __init__(self, config = {}):
    # Adds the path to the application to ease importing.
    # Allows for things like: "from myapp.models import *"
    #app_directory, app_file = os.path.split(app.__file__)
    #sys.path.append(os.path.join(app_directory, os.pardir))
    pass
  def process(self, request, flags):
    method, params = self._match_route(request.path)
    # See if it is an instance method of a class, and if it is, get that class.
    try:
      klass = method.im_class
    except AttributeError: klass = None
    if klass:
      # If you get a class, then instantiate it and call it's bound method.
      klass_instance = klass()
      bound_method = klass_instance.__getattribute__(method.__name__)
      status, data = bound_method(request, params)
      #print klass_instance.__dict__[method.__name__].__call__(self, params)
      #print klass.__dict__[method.__name__].__call__(klass, self, params)
    else:
      # Otherwise just call the simple method.
      status, data = method(request, params)
    # Debugging
    print status
    print data
    return (0,0,0)
  def _match_route(self, path):
    # Iterate through routes and find which matches
    for route in self.routes:
      route_result = route.match(path)
      if route_result:
        # If it does match, return the route.
        return route_result
    # It didn't match, then the pointer will end up here and raise the
    # route not matched Exception.
    raise Exception(404, 'Route not matched')