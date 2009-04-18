import os, sys

from controller import Expose, Filter

# Core class.
# TODO: Improve upon core class.
class Constrictor(object):
  # Importing version number and representation function.
  import __init__ as version
  # Sub-classing:
  # - Controller
  from controller import Controller
  from router import Route
  from request import Request
  
  # Listing controllers. Will likely be removed in favor of the routing system,
  # which is in development.
  controllers = []
  routes = []
  # Initialization
  def __init__(self):
    # Adds the path to the application to ease importing.
    # Allows for things like: "from myapp.models import *"
    #app_directory, app_file = os.path.split(app.__file__)
    #sys.path.append(os.path.join(app_directory, os.pardir))
    pass
  def process(self, path, headers, get, post):
    # Iterate through routes and find which matches
    for route in self.routes:
      route_result = route.match(path)
      if route_result:
        # If it does match, set route to the route_result and break the loop.
        route = route_result
        break
      # If it doesn't match, set route object to None to raise the exception
      # if it's the last route.
      else: route = None
    if not route:
      # It didn't match, raise Exception.
      raise Exception(404, 'Route not matched')
    # Grab result data from routing.
    controller = route[0]
    method = route[1]
    args = route[2]
    # Set up the request object, will be truly utilized later on, right now 
    # it's only used for providing GET and POST variables
    request = self.Request(path, headers, get, post)
    # Instantiate controller to pass to method call.
    controller_instance = controller()
    result = method(controller_instance, request, args)
  # Stubbing out methods
  def register_controller(self, controller):
    self.controllers.append(controller)