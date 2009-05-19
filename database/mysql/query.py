#import re

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
    # Either takes the given name or strips the Model off of 'TableModel'
    cls.Table = cls.Model.Table or cls.Model.__name__.lower()[:5]
    print cls.__dict__
    super(IntelligentQuery, cls).init(mysql)