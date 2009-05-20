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
    if type(args[0]) is str: # get('first'[, ...])
      # Check for keyword first arguments
      pos = args[0]
      if pos.lower() == 'first':
        single = True
        ret = cls._get_single(**kwargs)
      elif pos.lower() == 'all':
        ret = cls._get_all(**kwargs)
      elif pos.lower() == 'last':
        single = True
        raise Exception, 'ImplementationDoesNotExist: Last row functionality'
      else: raise Exception, 'Position unknown (Not "first", "last", or "all")'
    else: # get(1[, 2, 3[, ...]])
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
    if kwargs.has_key('include'):
      if not (kwargs['include'] is list or kwargs['include'] is tuple):
        include = [kwargs['include']]
      else: include = kwargs['include']
      for i in include:
        for field in cls.Model.Structure:
          if type(field) is mysql_fields.foreign:
            model = cls.mysql.get_model(field.model)
            if type(i) is str:
              if not i == model.Table: continue
            else:
              if not i is model: continue
        foreign_ids = [m.__getattribute__(field.name) for m in ret]
        unique_foreign_ids = cls._unique_list(foreign_ids)
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
    # always_list flag tells it to always return a list, simply setting it
    # implies truth.
    if single and not kwargs.has_key('always_list'): return ret[0]
    return ret
  @classmethod
  def _get_all(cls, **kwargs):
    # FIXME: Make this handle foreign keys and other fun stuff.
    try:
      conditions = kwargs['conditions']
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
  def _get_single(cls, *args, **kwargs):
    kwargs['limit'] = 1
    return cls._get_all(**kwargs)
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