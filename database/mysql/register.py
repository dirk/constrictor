from inspect import isfunction, ismethod

class register(object):
  """
  Simple class for registering models.
  Enables syntax like mysql.register.model(User)
  """
  mysql = None
  def __init__(self, mysql):
    self.mysql = mysql
  def model(self, *model):
    """Registers a model and loads it into the database client instance."""
    for m in model:
      m.Register()
      self.mysql.models.append(m)
  def query(self, *query):
    """Does the same as register.model except with a Query."""
    for q in query:
      q.Register()
      self.mysql.queries.append(q)