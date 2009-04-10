import os, sys

# Core class.
# TODO: Improve upon core class.
class constrictor(object):
  version = "0.0.1"
  # Defining controllers.
  controllers = []
  def __init__(self, app):
    # Adds the path to the application to ease importing.
    # Allows for things like: "from myapp.models import *"
    app_directory, app_file = os.path.split(app.__file__)
    sys.path.append(os.path.join(app_directory, os.pardir))
  def register_controller(self, controller):
    self.controllers.append(controller)
  # Instantiate a new controller test. (Watch the output that it prints!)