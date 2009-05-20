from copy import copy

class Model(object):
  """
  Base model class.
  """
  ismodel = True
  # Name of the table in the database.
  Table = None
  Query = None
  # Contains a list of the fields in the table.
  Structure = []
  _original = None
  def print_structure(self):
    print self.structure
  
  def save(self):
    self.Qu
  def diff(self):
    """
    Calculates the difference between the original (When first grabbed from the
    database) and the current version.
    """
    diff = {}
    for f in self.Structure:
      curr = f.query(self.__getattribute__(f.name))
      orig = f.query(self._original[f.name])
      if not curr == orig: diff[f.name] = curr
    return diff
  def __setattr__(self, key, value):
    # Check to see if all the values in the Structure have been set, and if
    # they have, save a copy in the _original variable.
    if not self._original and self.__dict__.has_key(self.Structure[-1].name):
      d = {}
      for f in self.Structure:
        d[f.name] = self.__getattribute__(f.name)
      self.__dict__['_original'] = d
    self.__dict__[key] = value
    
    