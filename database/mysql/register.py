from inspect import isfunction, ismethod

class register(object):
  """
  Simple class for registering models.
  Enables syntax like mysql.register.model(User)
  """
  mysql = None
  def __init__(self, mysql):
    self.mysql = mysql
  def model(self, model, add_to_class = True):
    """Registers a model and loads it into the database client instance."""
    # Allows for a list or tuple to be given, so that you can register more 
    # than one model at a time.
    if type(model) is list or type(model) is tuple:
      for m in model:
        self.mysql.models.append(m)
        if add_to_class:
          m.mysql = self.mysql
    else:
      self.mysql.models.append(model)
      if add_to_class:
        model.mysql = self.mysql
  def query(self, query):
    """Does the same as register.model except with a Query. NOTE: Only takes one Query"""
    query.init()
    self.mysql.queries.append(query)