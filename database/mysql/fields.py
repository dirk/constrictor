# Default, cookie-cutter field. (Mainly for reference.)
class Field(object):
  """
  Methods:
  generate: Returns the SQL required to generate the field in the database.
  empty: Returns the appropriate object (integer, string, etc.) for an empty
         field. Used when creating a new model.
  """
  creation_counter = 0
  name = None
  null = True
  # All fields require a name corresponding to their name in the table.
  def __init__(self):
    # Took forever to figure this out, then discovered that Django already did
    # it... Dangit.
    self.creation_counter = Field.creation_counter
    Field.creation_counter += 1
  def __cmp__(self, other):
    # Used for sorting fields on Model initialization.
    return cmp(self.creation_counter, other.creation_counter)
  def generate(self): pass
  def empty(self): pass
class Integer(Field):
  unsigned = True
  auto_increment = False
  def __init__(self, null = True, unsigned = True, auto_increment = False):
    # Basic asignments
    self.null = null
    self.unsigned = unsigned
    self.auto_increment = auto_increment
    super(Integer, self).__init__()
  def generate(self):
    base = 'bigint(20)'
    # NULL
    if self.null: base += ' NULL'
    else: base += ' NOT NULL'
    # auto_increment
    if self.auto_increment: base += ' auto_increment'
    # Resulting syntax
    return base
  def empty(self): return 0
class Primary(Integer):
  # Eventually make it actually perform like a true primary field.
  def __init__(self, unsigned = True, auto_increment = True):
    # Basic asignments
    self.null = False
    self.unsigned = unsigned
    self.auto_increment = auto_increment
    super(Integer, self).__init__()
class Foreign(Integer):
  "Represents a foreign key in a model. EG: category_id for a post"
  name = None
  model = None
  def __init__(self, model, null = True, unsigned = True):
    self.model = model
    super(Foreign, self).__init__(null, unsigned)
class String(Field):
  """
  Basic string field. Doesn't override the default result method since the 
  database will already send back a string.
  """
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
  def empty(self): return ''
class Text(Field):
  def __init__(self, null = True):
    self.null = null
    super(Text, self).__init__()
  def generate(self):
    base = 'text'
    if self.null: base += ' NULL'
    else: base += ' NOT NULL'
    # Resulting syntax
    return base
  def empty(self): return ''
class Boolean(Field):
  """
  Very basic boolean field.
  """
  def __init__(self, null = True):
    self.null = null
    super(Boolean, self).__init__()
  def empty(self): return False