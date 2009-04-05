# Ok, just getting start with the framework
"""
Just outlining the base system.

Core: Contains basic code for interfacing all of the different aspects together.
Core.Controller: Inherited by actual controllers, holds operations that power (and provide 
                 functionality for)  controllers.
Core.Model: Used for defining models to be used in the database.
Core.Query: Used for defining queries to be executed on the database.
Core.Query.Database: Interfaces with databases. (Currently only MySQL.)
Core.Query.IQ: Short for Intelligent Query. The system designed to mimic Ruby on Rails' 
               ActiveRecord functionality.
Core.Templating: Engine used for templating.

^ All of that is crap, ignore it.
"""

import os, sys

class constrictor(object):
  version = "0.0.1"
  # Defining controllers, models, and queries
  controllers = []
  def __init__(self, app):
    # Adds the path to the application to ease importing.
    # Allows for things like: "from myapp.models import *"
    app_directory, app_file = os.path.split(app.__file__)
    sys.path.append(os.path.join(app_directory, os.pardir))
  def register_controller(self, controller):
    self.controllers.append(controller)
  # Instantiate a new controller test. (Watch the output that it prints!)