# Default, cookie-cutter field. (Mainly for reference.)
class Field(object):
  """
  Methods:
  query: Gets passed the data to be inserted into an INSERT or UPDATE 
         MySQL query. Expected to return data formatted for proper 
         querying.
  result: Gets passed the raw data from the MySQL query. Expected to 
          return a properly process/formatted piece of data to be 
          inserted into the actual model.
  generate: Returns the SQL required to generate the field in the database.
  """
  creation_counter = 0
  name = None
  # All fields require a name corresponding to their name in the table.
  def __init__(self):
    # Took forever to figure this out, then discovered that Django already did
    # it... Dangit.
    self.creation_counter = Field.creation_counter
    Field.creation_counter += 1
  def __cmp__(self, other):
    # Used for sorting fields on Model initialization.
    return cmp(self.creation_counter, other.creation_counter)
  def generate(self):
    return 'int(11)'
  def query(self, data):
    return data
  def result(self, data):
    return data

class Integer(Field):
  """
  Basic integer field. Query and result methods merely perform an int() upon 
  the given data.
  
  Properties: null (boolean), unsigned (boolean), primary (boolean), 
              auto_increment (boolean)
  """
  null = True
  unsigned = True
  primary = False
  auto_increment = False
  def __init__(self, null = True, unsigned = True, primary = False, \
    auto_increment = False):
    # Basic asignments
    self.null = null
    self.unsigned = unsigned
    self.primary = primary
    self.auto_increment = auto_increment
    super(Integer, self).__init__()
  def generate(self):
    base = 'int(11)'
    # NULL
    if self.null: base += ' NULL'
    else: base += ' NOT NULL'
    # auto_increment
    if self.auto_increment: base += ' auto_increment'
    # Resulting syntax
    return base
  def query(self, data):
    if self.unsigned is True:
      return int(data)
    else:
      return data
  result = query
class Primary(Integer):
  # Eventually make it actually perform like a true primary field.
  pass
class Foreign(Integer):
  "Represents a foreign key in a model. EG: category_id for a post"
  name = None
  model = None
  def __init__(self, model, null = True, unsigned = True):
    self.model = model
    super(Foreign, self).__init__(null, unsigned)
  def query(self, data):
    if type(data) is int or type(data) is str:
      return int(data)
    else:
      # TODO: Make it get a primary field, not just default to ID
      return int(data.id)
  result = query
class String(Field):
  """
  Basic string field. Doesn't override the default result method since the 
  database will already send back a string.
  """
  null = True
  length = 255
  def __init__(self, null = True, length = 255):
    self.null = null
    self.length = length
    super(String, self).__init__()
  def generate(self):
    base = 'varchar(' + str(self.length) + ')'
    # NULL
    if self.null: base += ' NULL'
    else: base += ' NOT NULL'
    # Resulting syntax
    return base
  def query(self, data):
    """Doing a str() on the data just to be safe."""
    return str(data)

class Boolean(Field):
  """
  Very basic boolean field.
  """
  null = True
  def __init__(self, null = True):
    self.null = null
    super(Boolean, self).__init__()
  def generate(self):
    base = 'tinyint(1)'
    # NULL
    if self.null: base += ' NULL'
    else: base += ' NOT NULL'
    # Resulting syntax
    return base
  def query(self, data):
    # First, try to boolean it (to catch "True", "False", "T", and "F", 
    # which int doesn't catch), then int it for insertion into the database.
    try:
      data = bool(data)
    finally:
      return int(data)
  def result(self, data):
    if int(data): return True
    else: return False

# This is derived from some database. I don't remember where; but it's here 
# for reference.
"""
`id` int(11) NOT NULL auto_increment,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `password` varchar(128) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `last_login` datetime NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY  (`id`),
  UNIQUE KEY `username` (`username`)
"""
