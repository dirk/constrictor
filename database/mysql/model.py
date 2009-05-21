from copy import copy
from query import Query
import fields as mysql_fields

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
  # List of attributes that can be set by mass assignment.
  Accessible = ['username']
  
  def __init__(self, attribs = None, silent = True):
    # Assignment by attribute
    if type(attribs) is dict:
      for attr in attribs:
        if self.Accessible:
          try:
            n = self.Accessible.index(attr);del(n)
            self.__setattr__(attr, attribs[attr])
          except ValueError:
            if not silent:
              error = '"%s" cannot be assigned via mass-assignment' % attr
              raise Exception, error
        else:
          self.__setattr__(attr, attribs[attr])
          
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
      curr = f.result(self.__getattribute__(f.name))
      orig = f.result(self._original[f.name])
      if not curr == orig: diff[f.name] = curr
    return diff
  def save(self):
    # If it doesn't have an ID (Either nonexistant or not set), then call the
    # create() method to do an INSERT instead of an UPDATE.
    try:
      if not self.id: self.create()
    except AttributeError: self.create()
    base = 'UPDATE %s SET ' % self.Table
    diff = self.diff()
    fields = ''
    if not diff: return None
    for key in diff:
      field = self._get_field_by_name(key)
      value = field.query(diff[key])
      fields += ', ' + field.name + ' = ' + Query.format_type(value)
    base += fields[2:] + ' WHERE id = ' + str(self.id)
    Query.query(base)
    return self
  def create(self):
    base = 'INSERT INTO %s ' % self.Table
    names = []
    values = []
    for f in self.Structure:
      try:
        name = f.name
        value = Query.format_type(f.query(self.__getattribute__(name)))
        names.append(name);values.append(value)
      except AttributeError:
        # TODO: Make check for primary and not default to 'id'
        if not f.null and \
          f.name != 'id': raise Exception, 'Field "%s" cannot be null' % f.name
    base += '(%s) ' % (', '.join(names))
    base += 'VALUES (%s)' % (', '.join(values))
    self.Query.query(base)
    self._original = self._build_original()
    return self
  new = create
  def _get_field_by_name(self, name):
    for f in self.Structure:
      if f.name == name: return f
  def _build_original(self):
    d = {}
    for f in self.Structure:
      try:
        d[f.name] = self.__getattribute__(f.name)
      except AttributeError: pass
    return d
  def __setattr__(self, key, value):
    # Check to see if all the values in the Structure have been set, and if
    # they have, save a copy in the _original variable.
    if not self._original and self.__dict__.has_key(self.Structure[-1].name):
      self.__dict__['_original'] = self._build_original()
    self.__dict__[key] = value
    
    