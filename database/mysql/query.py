import re

class Query(object):
  """
  System for querying the database in an speedy and efficient mannger.
  """
  # Reference to MySQL client (constrictor.database.mysql.__init__.mysql).
  mysql = None
  # Human- and code-friendly name of the Query
  name = 'query'
  
  # Methods:
  def query(self):
    """
    Actually executes the query and processes the database results.
    """
      