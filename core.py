import os, sys

from controller import Expose, Filter
from session import SessionStore
from utils import recursive_merge, get_default_favicon

class Constrictor(object):
  # Importing version number and representation function.
  import __init__ as version
  # Sub-classing:
  from controller import Controller
  from router import Route
  # - Request class used in routing and processing system.
  from request import Request
  
  session = None # Will hold the session storage object.
  routes = [] # List of routes
  config = {
    'Session': {
      # Tells whether Constrictor should even use Sessions.
      'Use': False,
      'Security': {
        'Check IP': False,
      },
      # Defines storage engine Constrictor should use.
      # (EG: memcached and MySQL interfaces)
      'Store': SessionStore,
    },
    'Favicon': {
      # Allows you set an image (raw data) and content type that will be sent
      # when "/favicon.ico" is requested.
      'Data': get_default_favicon(),
      'Content-type': 'image/gif'
    }
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
    #for key in config: self.config[key] = config[key]
  def process(self, request):
    # If sessions are enabled, attempt to retrieve a session. (via Request)
    if self.config['Session']['Use']:
      request.session = self.session.retrieve(request) or self.session.create(request)
    try:
      method, params = self._match_route(request.path)
    except Exception, e:
      if e[0] == 404:
        print request.ip_address + ': "' + request.path + '" > 404: Not Found!'
        request.status = 404
        # TODO: Allow changing of 404 message
        custom_404 = \
"""
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL {path} was not found on this server.</p>
</body></html>
"""
        return (custom_404.replace('{path}', request.path), 'Special')
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