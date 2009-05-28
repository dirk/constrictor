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
  Accessible = []
  
  def __init__(self, attribs = None, silent = True, force = False):
    if type(attribs) is dict:
      self.attributes(attribs, silent, force)
  @classmethod
  def Register(cls):
    """
    Called by mysql.register.model(). Tells the model to process itself and
    extract its fields into Model.Structure.
    """
    f = [mysql_fields.__getattribute__(k) for k in mysql_fields.__dict__]
    fields = []
    for key in cls.__dict__:
      attr = type.__getattribute__(cls, key)
      if type(attr) in f:
        fields.append((key, attr))
    fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))
    for name, field in fields: field.name = name
    cls.Structure = [f[1] for f in fields]
  def attributes(self, attribs, silent = True, force = False):
    # Assignment by attribute
    for attr in attribs:
      # Check if the person has defined a list of Accessible attributes,
      # otherwise just assign 'em all.
      if self.Accessible and not force:
        # See if it's in the the Acccessible list.
        try:
          n = self.Accessible.index(attr);del(n)
          self.__setattr__(attr, attribs[attr])
        except ValueError:
          # Either raise an error, or just let it pass silently
          if not silent:
            error = '"%s" cannot be assigned via mass-assignment' % attr
            raise Exception, error
      else:
        self.__setattr__(attr, attribs[attr])
  def diff(self):
    """
    Calculates the difference between the original (When first grabbed from the
    database) and the current version.
    """
    diff = {}
    for f in self.Structure:
      try:
        curr = f.result(self.__getattribute__(f.name))
        orig = f.result(self._original[f.name])
        if not curr == orig: diff[f.name] = curr
      except AttributeError:
        # For some reason, the attribute wasn't in either namespace, so see if
        # it exists in the current one, and if it does, then it wasn't assigned
        # in the original and is most definitely a difference.
        if self.__dict__.has_key(f.name): diff[f.name] = curr
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
    # Build field and value list if there is a difference
    for key in diff:
      field = self._get_field_by_name(key)
      value = field.query(diff[key])
      fields += ', ' + field.name + ' = ' + Query.format_type(value)
    base += fields[2:] + ' WHERE id = ' + str(self.id)
    Query.query(base)
    # Right now, just spit back the instance of self
    return self
  def create(self):
    base = 'INSERT INTO %s ' % self.Table
    names = []
    values = []
    for f in self.Structure:
      try:
        # Try to get the attribute, else raise an exception if it can't be null.
        name = f.name
        value = Query.format_type(f.query(self.__getattribute__(name)))
        names.append(name);values.append(value)
      except AttributeError:
        # TODO: Make check for primary and not default to 'id'
        if not f.null and \
          f.name != 'id': raise Exception, 'Field "%s" cannot be null' % f.name
    # Build the set of fields and VALUES.
    base += '(%s) ' % (', '.join(names))
    base += 'VALUES (%s)' % (', '.join(values))
    # Execute and dump the current instance's attribs into the _original.
    self.Query.query(base)
    self._original = self._build_original()
    # Spit yourself back!
    return self
  new = create
  def _get_field_by_name(self, name):
    for f in self.Structure:
      if f.name == name: return f
  def _build_original(self):
    # Build a dict of the current instances attribs.
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
    
    