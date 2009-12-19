import fields as mysql_fields

class Model(object):
  ismodel = True
  mysql = None
  Table = None
  Structure = []
  _original = {}
  # List of attributes that can be set by mass assignment.
  Accessible = []
  
  def __init__(self, attribs = None, silent = True, force = False):
    for f in self.Structure: self.__setattr__(f.name, '')
    if type(attribs) is dict:
      self.attributes(attribs, silent, force)
  def attributes(self, attribs, silent = True, force = False):
    # Assignment by attribute
    for field in self.Structure:
      attr = field.name
      if attr in attribs.keys():
        # Check if the person has defined a list of Accessible attributes,
        # otherwise just assign 'em all.
        if self.Accessible and not force:
          # See if it's in the the Acccessible list.
          if attr in self.Accessible:
            self.__setattr__(attr, attribs[attr])
          else:
            if not silent:
              error = '"%s" cannot be assigned via mass-assignment' % attr
              raise Exception, error
        else:
          self.__setattr__(attr, attribs[attr])
  @classmethod
  def Register(cls):
    """
    Called by mysql.register.model(). Tells the model to process itself and
    extract its fields into Model.Structure.
    """
    # Get the list of fields
    f = [mysql_fields.__getattribute__(k) for k in mysql_fields.__dict__]
    fields = []
    for key in cls.__dict__:
      # Check if the attribute is a field
      attr = type.__getattribute__(cls, key)
      if type(attr) in f: fields.append((key, attr))
    # Sort them by their creation_counter
    fields.sort(lambda x, y: cmp(x[1].creation_counter, y[1].creation_counter))
    # Iterate through the fields
    for name, field in fields:
      field.name = name # # Assign the name
      if type(field) is mysql_fields.Primary:
        type.__delattr__(cls, name)
      else:
        if field.null is True:
          type.__setattr__(cls, field.name, None)
        else:
          type.__setattr__(cls, field.name, field.empty())
    # Store the structure
    cls.Structure = [f[1] for f in fields]
  @classmethod
  def get(cls, *items, **options):
    #print options
    cls._parse_options(options)
    cls._parse_conditions(options)
    if items:
      flag = cls._parse_items(items, options)
      if flag: return flag
    fields = cls._build_fields()
    base = 'SELECT %s FROM `%s`' % (fields, cls.Table)
    if options['where']:
      base += ' WHERE ' + options['where']
    if options['limit']:
      base += ' LIMIT ' + str(options['limit'])
      if options['offset']:
        base += ' OFFSET ' + str(options['offset'])
    ret = cls._parse_result(cls.mysql.query(base))
    return cls._parse_include(ret, **options)
  @classmethod
  def first(cls, *items, **options):
    options['limit'] = 1
    ret = cls.get(*items, **options)
    if ret.__len__() > 0: return ret[0]
  @classmethod
  def _parse_include(cls, rows, **options):
    includes = options['include']
    if includes:
      foreign_fields = [f for f in cls.Structure if type(f) is \
        mysql_fields.Foreign]
      if not (type(includes) is list or type(includes) is tuple):
        includes = [includes]
      if foreign_fields.__len__() > 0:
        # If it is child accessing parent.
        for include in includes:
          field = [f for f in foreign_fields if f.model is include][0]
          name = field.name
          if name.endswith('_id'):
            name = name[:-3]
          foreign_ids = []
          for m in rows:
            id = m.__getattribute__(field.name)
            if id is not None: foreign_ids.append(id)
          unique_foreign_ids = cls._unique_list(foreign_ids)
          # Grab the foreign objects.
          children = include.get(*unique_foreign_ids)
          # Get the foreign models primary key.
          foreign_primary = include.get_primary()
          for r in rows:
            for c in children:
              if c.__getattribute__(foreign_primary.name) == \
                r.__getattribute__(field.name):
                r.__setattr__(name, c)
      else:
        pass # It is parent including its children
    return rows
  def save(self):
    if self._original:
      diff = self.diff()
      if diff:
        base = 'UPDATE `%s` SET ' % self.Table
        sets = []
        for key in diff:
          sets.append('`%s` = %s' % (key, self.format_type(diff[key])))
        base += ', '.join(sets)
        primary = self.get_primary()
        base += ' WHERE %s = %s' % (primary.name, self.__getattribute__(primary.name))
        self.mysql.query(base);self.save_original()
    else:
      self.create()
    return self
  def diff(self):
    diff = {}
    for f in self.Structure:
      try:
        value = self.__getattribute__(f.name)
        if not value and value != 0: raise AttributeError
        if self._original.has_key(f.name):
          if f.name.endswith('_id') and type(f) is mysql_fields.Foreign:
            try:
              foreign = self.__getattribute__(f.name[:-3])
              primary = foreign.get_primary()
              if foreign.__getattribute__(primary.name) != self._original[f.name]:
                diff[f.name] = foreign.__getattribute__(primary.name)
            except AttributeError: pass
            if self.__getattribute__(f.name) != self._original[f.name]:
              diff[f.name] = self.__getattribute__(f.name)
          elif self.__getattribute__(f.name) != self._original[f.name]:
            diff[f.name] = self.__getattribute__(f.name)
      except AttributeError:
        if f.null is False:
          raise Exception, 'Field "%s" cannot be null!' % f.name
        else:
          diff[f.name] = 'NULL'
    return diff
  def create(self):
    diff = self.get_create_dict()
    keys = diff.keys()
    values = diff.values()
    base = 'INSERT INTO `%s` (' % self.Table
    base += ', '.join(['`' + key + '`' for key in keys]) + ') '
    base += 'VALUES (' + ', '.join([self.format_type(value) for value in values]) + ')'
    self.mysql.query(base);self.save_original()
  def get_create_dict(self):
    ret = {}
    for f in self.Structure:
      try:
        if type(f) is mysql_fields.Primary: continue
        value = self.__getattribute__(f.name)
        if not value and value != 0: raise AttributeError
        if f.name.endswith('_id') and type(f) is mysql_fields.Foreign:
          try:
            foreign = self.__getattribute__(f.name[:-3])
            primary = foreign.get_primary()
            ret[f.name] = foreign.__getattribute__(primary.name)
          except AttributeError:
            ret[f.name] = value
        else:
          ret[f.name] = value
      except AttributeError:
        if f.null is False:
          raise Exception, 'Field "%s" cannot be null!' % f.name
        else:
          ret[f.name] = 'NULL'
    return ret
  @classmethod
  def _parse_items(cls, items, options):
    if type(items[0]) is str:
      flag = items[0].lower()
      if flag == 'first':
        return cls.first(**options)
      else: return
    else:
      primary = cls.get_primary().name
      options['where'] = ' OR '.join([('`' + primary + '` = ' + str(item)) \
        for item in items])
      return
  @classmethod
  def _parse_result(cls, rows):
    ret = []
    for r in rows:
      model = cls()
      c = 0
      for f in cls.Structure:
        item = r[c]
        if item is None:
          item = None
        # Try to do appropriate typecasting based on the field.
        elif type(f) is mysql_fields.Boolean:
          item = bool(item)
        elif type(f) is mysql_fields.Integer or type(f) is \
          mysql_fields.Primary or type(f) is mysql_fields.Foreign:
          item = int(item)
        else: item = str(item) # Fallback to string
        model.__dict__[f.name] = item
        c += 1 # Increment field counter for row tuple.
      model.save_original() # Duh
      ret.append(model)
    return ret
  @classmethod
  def _parse_options(cls, options):
    keys = ['where', 'limit', 'offset', 'include', 'no_escape']
    for key in keys:
      if not options.has_key(key):
        options[key] = None
  @classmethod
  def _parse_conditions(cls, options):
    conditions = options['where']
    # If it's a string, don't even bother with it.
    if conditions is not None and not type(conditions) is str:
      variables = conditions[1:]
      conditions = conditions[0]
      # Go through variables (optionally escape) and sub them into the string
      for var in variables:
        if options['no_escape']:
          var = cls.format_type(var, False)
        else: var = cls.format_type(var)
        conditions = conditions.replace('?', str(var), 1)
      options['where'] = conditions
  @classmethod
  def _build_fields(cls): return ', '.join(['`' + f.name + '`' for f in cls.Structure])
  @classmethod
  def format_type(cls, item, escape = True):
    """
    Formats:
    - String: With quotes (Escaped if second param is True, which is default)
    - Integer (int, float, long): Just the string
    - None or 'null': 'NULL
    """
    t = type(item)
    if item is None:
      return 'NULL'
    elif t is str:
      # Handle string
      if item.lower() == 'null':
        return 'NULL'
      elif escape:
        return '"' + cls.escape(item) + '"'
      else:
        return '"' + item + '"'
    elif t is bool: return int(t)
    elif t is int or t is float or t is long or t is mysql_fields.Primary \
      or t is mysql_fields.Foreign: return str(item)
    # Give up
    else: raise TypeError, 'Unformattable type: %s' % type(item)
  @classmethod
  def _unique_list(cls, l):
    r = []
    for i in l:
      if not i in r: r.append(i)
    return r
  def save_original(self):
    # Build a dict of the current instances attribs.
    d = {}
    for f in self.Structure:
      try:
        d[f.name] = self.__getattribute__(f.name)
      except AttributeError: pass
    self.__dict__['_original'] = d
  @classmethod
  def get_primary(cls):
    for field in cls.Structure:
      if type(field) is mysql_fields.Primary: return field
  @classmethod
  def escape(cls, item): return cls.mysql.database.escape_string(item)