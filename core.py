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
  # - Route class for routing system
  from router import Route
  # - Request class used in routing and processing system.
  from request import Request
  
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
    # Set up the request object, will be truly utilized later on, right now 
    # it's only used for providing GET and POST variables
    request = self.Request(path, headers, get, post)
    if route[0] is None:
      # No controller for method.
      method = route[1]
      args = route[2]
      # Just execute the method.
      result = method(request, args)
    else:
      # Grab result data from routing.
      controller = route[0]
      method = route[1]
      args = route[2]
      # Instantiate controller to pass to method call.
      controller_instance = controller()
      # Grab the before and after filters
      after_filters = controller_instance.after_filters()
      before_filters = controller_instance.before_filters()
      # --------------------------------
      # Actual juicy part of the system.
      # Process before filters.
      for func in before_filters:
        func(request, args)
      # Call the method itself!
      result = method(controller_instance, request, args)
      # Process after filters.
      for func in after_filters:
        func(request, args)
    return result