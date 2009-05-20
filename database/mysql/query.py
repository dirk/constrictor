#import re
import fields as mysql_fields

class Query(object):
  """
  System for querying the database in an speedy and efficient mannger.
  """
  # Reference to MySQL client (constrictor.database.mysql.__init__.mysql).
  mysql = None
  # Human- and code-friendly name of the Query
  name = 'query'
  
  @classmethod
  def init(cls, mysql):
    """
    Called by mysql.register.query(). Puts the passed MySQLdb object into the
    local variable 'mysql.'
    """
    cls.mysql = mysql
  @classmethod
  def _query(cls, query):
    """Actually executes the query and processes the database results."""
    cursor = cls.mysql.database.cursor()
    cursor.execute(query)
    return cursor.fetchall()

class IntelligentQuery(Query):
  """
  Extends base Query system and adds more functionality and 'intelligence.'
  """
  # Requires a model class to do intro/extrospection.
  Model = None
  Table = None
  @classmethod
  def init(cls, mysql):
    cls.Model.Query = cls
    # Either takes the given name or strips the Model off of 'TableModel'
    cls.Table = cls.Model.Table or cls.Model.__name__.lower()[:5]
    super(IntelligentQuery, cls).init(mysql)
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
            elif not include is model:
              continue
            else: break
        # Grab list of IDs from the result set, then make the list unique.
        foreign_ids = [m.__getattribute__(field.name) for m in ret]
        unique_foreign_ids = cls._unique_list(foreign_ids)
        # Use the IQ of the foreign model to grab the foreign objects.
        children = model.Query.get(*unique_foreign_ids, always_list = True)
        
        name = field.name
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
    try:
      if kwargs.has_key('where'):
        conditions = kwargs['where']
      else: conditions = kwargs['conditions']
    except KeyError: conditions = None
    
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
    rows = cls._query(base)
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
  def _conditions(cls, cons):
    "Takes list of conditions and parses them."
    for con in cons:
      print con
  @classmethod
  def _unique_list(cls, l):
    r = []
    for i in l:
      if not i in r: r.append(i)
    return r
  # Alias get as find for those coming from Rails. Just to be nice.
  find = get