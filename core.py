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
  
  # Listing controllers. Will likely be removed in favor of the routing system,
  # which is in development.
  controllers = []
  # Initialization
  def __init__(self):
    # Adds the path to the application to ease importing.
    # Allows for things like: "from myapp.models import *"
    #app_directory, app_file = os.path.split(app.__file__)
    #sys.path.append(os.path.join(app_directory, os.pardir))
    pass
  # Stubbing out methods
  def register_controller(self, controller):
    self.controllers.append(controller)