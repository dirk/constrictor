#import re
import fields as mysql_fields

class Query(object):
  """
  Extends base Query system and adds more functionality and 'intelligence.'
  """
  # Requires a model class to do intro/extrospection.
  Model = None
  Table = None
  @classmethod
  def init(cls, mysql):
    cls.mysql = mysql
    cls.Model.Query = cls
    # Either takes the given name or strips the Model off of 'TableModel'
    cls.Table = cls.Model.Table or cls.Model.__name__.lower()[:5]
  @classmethod
  def query(cls, query):
    """Actually executes the query and processes the database results."""
    cursor = cls.mysql.database.cursor()
    cursor.execute(query)
    return cursor.fetchall()
  @classmethod
  def get(cls, *args, **kwargs):
    """
    Current kwargs: include, limit, always_list
    """
    single = False
    if len(args) > 0: # get(1[, 2, 3[, ...]])
      # Check for ID-based arguments
      if len(args) is 1: single = True
      # Build string of conditions from the list of IDs
      for f in cls.Model.Structure:
        # FIXME: Change to primary from integer
        if type(f) is mysql_fields.integer:
          primary = f; break
      cons = ' OR '.join([(primary.name + ' = ' + str(x)) for x in args])
      kwargs['conditions'] = cons
      ret = cls._get_all(**kwargs)
    else:
      ret = cls._get_all(**kwargs)
    cls._parse_include(kwargs, ret)
    # always_list flag tells it to always return a list, simply setting it
    # implies truth.
    if single and not kwargs.has_key('always_list'): return ret[0]
    return ret
  # Alias get as find for those coming from Rails. Just to be nice.
  find = get
  @classmethod
  def _parse_include(cls, kwargs, ret):
    """
    Takes an include (String or Model) statement, fetches all the rows with
    IDs from the result set, and adds those rows to the result set.
    
    TODO: Improve this documentation
    """
    if kwargs.has_key('include'):
      # Make include into a list (if it's not) so that it's always iterable.
      if not (kwargs['include'] is list or kwargs['include'] is tuple):
        include = [kwargs['include']]
      else: include = kwargs['include']
      for i in include:
        # Iterate over each include statement and the fields in the model.
        for field in cls.Model.Structure:
          if type(field) is mysql_fields.foreign:
            model = cls.mysql.get_model(field.model)
            if type(include) is str:
              if not include == model.Table: continue
            elif not include is model: continue
            else: break
        # Grab list of IDs from the result set, then make the list unique.
        foreign_ids = [m.__getattribute__(field.name) for m in ret]
        unique_foreign_ids = cls._unique_list(foreign_ids)
        # Use the IQ of the foreign model to grab the foreign objects.
        children = model.Query.get(*unique_foreign_ids, always_list = True)
        name = field.name # Make things simpler
        if name.endswith('_id'): name = name[:-3]
        # Iterate through result rows and assign the attribute to the child
        # if the IDs match.
        for m in ret:
          for child in children:
            # FIXME: Change to primary key instead of ID default
            if child.id == m.__getattribute__(field.name):
              m.__setattr__(name, child)
    return ret
  @classmethod
  def _get_all(cls, **kwargs):
    # If conditions are passed (Either as 'where' or 'conditions')
    conditions = cls._parse_conditions(kwargs)
    # Build list of fields, and add it to query base
    query_fields = ', '.join([f.name for f in cls.Model.Structure])
    base = 'SELECT %s FROM %s' % (query_fields, cls.Model.Table)
    # Handle conditions string and add it to query
    if conditions: base += ' WHERE ' + conditions
    # Handle limit numbers
    try:
      limit = kwargs['limit']
      base += ' LIMIT ' + str(limit)
    except KeyError: pass
    # Execute query
    rows = cls.query(base)
    # Building result set
    ret = []
    for r in rows:
      model = cls.Model()
      c = 0
      for f in cls.Model.Structure:
        model.__setattr__(f.name, f.result(r[c]))
        c += 1
      ret.append(model)
    return ret
  @classmethod
  def get_first(cls, **kwargs):
    # Fetches one row, passes kwargs to _get_all() with appended 'limit' statement.
    kwargs['limit'] = 1
    ret = cls._get_all(**kwargs)
    cls._parse_include(kwargs, ret)
    return ret[0]
  # Alias first() for get_first() for less characters.
  first = get_first
  @classmethod
  def _parse_conditions(cls, kwargs):
    "Takes list of conditions and parses them."
    try:
      # Grab 'dem conditions
      if kwargs.has_key('where'):
        conditions = kwargs['where']
      else: conditions = kwargs['conditions']
    except KeyError: return None
    # If it's a string, don't even bother with it.
    if type(conditions) is str:
      return conditions
    else:
      variables = conditions[1:]
      conditions = conditions[0]
      # Go through variables (optionally escape) and sub them into the string
      for var in variables:
        if kwargs.has_key('no_escape'):
          var = cls.format_type(var, False)
        else: var = cls.format_type(var)
        #print conditions
        conditions = conditions.replace('?', str(var), 1)
      return conditions
  @classmethod
  def format_type(cls, item, escape = True):
    """
    Formats:
    - String: With quotes (Escaped if second param is True, which is default)
    - Integer (int, float, long): Just the string
    """
    t = type(item)
    if t is str:
      # Handle string
      if escape:
        return '"' + cls.escape(item) + '"'
      else:
        return '"' + item + '"'
    # Y4Is: Yay for integers!
    elif t is int or t is float or t is long: return item
    # Give up
    else: raise TypeError, 'Unformattable type'
  @classmethod
  def _unique_list(cls, l):
    r = []
    for i in l:
      if not i in r: r.append(i)
    return r
  @classmethod
  def escape(cls, item): return cls.mysql.database.escape_string(item)