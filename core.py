import os, sys

from controller import Expose, Filter
from session import SessionStore
from utils import recursive_merge

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
  
  session = None
  
  config = {
    'Session': {
      # Tells whether Constrictor should even use Sessions.
      'Use': False,
      # Defines storage engine Constrictor should use.
      # (EG: memcached and MySQL interfaces)
      'Store': SessionStore,
    },
  }
  routes = []
  # Initialization
  def __init__(self, config = {}):
    # Adds the path to the application to ease importing.
    # Allows for things like: "from myapp.models import *"
    #app_directory, app_file = os.path.split(app.__file__)
    #sys.path.append(os.path.join(app_directory, os.pardir))
    
    # Recurively combine the original config with the passed configuration to
    # overwrite the original keys with any passed in config.
    recursive_merge(self.config, config)
    self.sessions = []
    # Test if sessions are enabled, and instantiate a instance of the session.
    if self.config['Session']['Use']:
      self.session = self.config['Session']['Store'](self)
    for key in config: self.config[key] = config[key]
  def process(self, request):
    # If sessions are enabled, tell the request to attempt to retrieve a
    # session.
    if self.config['Session']['Use']:
      request.session = self.session.retrieve(request)
    method, params = self._match_route(request.path)
    # Check if method has Expose attribute that is True.
    try:
      if not method.Expose is True: raise AttributeError
    except AttributeError:
      raise Exception, 'Method must be exposed!'
    # See if it is an instance method of a class, and if it is, get that class.
    try:
      klass = method.im_class
    except AttributeError: klass = None
    if klass:
      # If you get a class, then instantiate it and call it's bound method.
      klass_instance = klass()
      bound_method = klass_instance.__getattribute__(method.__name__)
      status, data = bound_method(request, params)
    else:
      # Otherwise just call the simple method.
      status, data = method(request, params)
    # If sessions are enabled, tell the session storage system to save the
    # current session.
    if self.config['Session']['Use']: self.session.save(request.session)
    return (status, data)
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