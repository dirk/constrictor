"""
New MVC-based ORM system. Replacing older QMCV system, which was inelegant in
it's implementation.
"""

# Import mysqldb module. (Must install yourself, not included with Python.)
import MySQLdb as mysqldb
# Auto-importing fields to make stuff easier.
import fields as Fields
from model import Model

class mysql(object):
  models = []
  def __init__(self, *auto_connect):
    """
    Optional four arguments (host, username, password, database) are passed
    to mysql.connect for auto-connect functionality.
    """
    # Establish database connection
    Model.mysql = self
    # Only connect if passed 4 parameters
    # TODO: Add more connection options for greater flexibility.
    if len(auto_connect) is 4: self.connect(*auto_connect)
  def connect(self, host, username, password, database):
    "Takes connection parameters and establishes a MySQLdb connection."
    self.database = mysqldb.connect(host = host, user = username, 
    passwd = password, db = database)
  def query(self, query):
    """Actually executes the query and processes the database results."""
    cursor = self.database.cursor()
    cursor.execute(query)
    # If it's a query that's expected to return a value (EG: SELECT)
    if query.strip().lower().startswith('select'): return cursor.fetchall()
  def register(self, *model):
    """Registers a model and loads it into the database client instance."""
    for m in model:
      m.Register()
      self.models.append(m)
  def close(self):
    self.database.close()