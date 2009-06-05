import os, sys

from controller import Expose, Filter
from session import SessionStore
from utils import recursive_merge, get_default_favicon, defaults
# Import Route for ease of use.
from router import Route, Controller_Route

class Constrictor(object):
  # Importing version number and representation function.
  import __init__ as version
  # Sub-classing:
  from controller import Controller
  from router import Route, Controller_Route
  # ^ Also imported here for convenience, I guess.
  # - Request class used in routing and processing system.
  from request import Request
  
  session = None # Will hold the session storage object.
  routes = [] # List of routes
  config = {
    'Session': {
      # Tells whether Constrictor should even use Sessions.
      'Use': False,
      'Security': {
        'Check IP': False, # Check IP address during session retrieval?
      },
      # Defines storage engine Constrictor should use.
      # (EG: SessionStore (local), memcached, MySQL, etc.)
      'Store': SessionStore,
    },
    'Security': {
      'Check Expose': False, # Check for Expose attribute on requested method?
    },
    'Favicon': {
      # Allows you set an image (raw data) and content type that will be sent
      # when "/favicon.ico" is requested.
      # NOTE: This crap is only for the development server.
      'Data': get_default_favicon(),
      'Content-type': 'image/gif'
    },
    'Pages': {
      404: defaults.Error_404, # Default 404 error page.
      # Default page for redirects (Used by Request.redirect).
      'Redirect': defaults.Redirect,
    },
  }
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
  def process(self, request):
    # If sessions are enabled, attempt to retrieve a session. (via Request)
    if self.config['Session']['Use']:
      request.session = self.session.retrieve(request) or self.session.create(request)
    # Get the method and URL segments, else return a 404 to the Server.
    try:
      method, params = self._match_route(request.path)
    except Exception, e:
      if e[0] == 404:
        request.status = 404
        page = self.config['Pages'][404].replace('{path}', request.path)
        debug = {'controller': None, 'method': 'Not Found', 'args': ()}
        return (page, debug)
      else: raise Exception, 'Unknown routing error!'
    if self.config['Security']['Check Expose']:
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
      # Instantiate the instance and retrieve its bound method.
      klass_instance = klass()
      bound_method = klass_instance.__getattribute__(method.__name__)
      # Go through filters, actual method is sandwhiched in between.
      for f in klass_instance.before_filters(): f(request, params)
      data = bound_method(request, params)
      for f in klass_instance.after_filters(): f(request, params)
    else:
      # Otherwise just call the simple method.
      data = method(request, params)
    # If sessions are enabled, tell the session storage system to save the
    # current session.
    if self.config['Session']['Use']: self.session.save(request.session)
    debug = {'controller': klass, 'method': method, 'args': params}
    return (data, debug)
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