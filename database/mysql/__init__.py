"""
MySQL backend API for Constrictor. Contains the revolutionary Model-Query 
systems.
"""
# Import Python modules.
import re
# Import mysqldb module. (Must install yourself, not included with Python.)
import MySQLdb as mysqldb

# Register utility to be bound into the database. Allows for something like 
# mysql.register.model or mysql.register.query.
from register import register
# Auto-importing fields to make stuff easier.
import fields
# Base model class.
from model import model

class mysql(object):
  database = None
  models = []
  queries = []
  def __init__(self, host, username, password, database):
    # Establish database connection
    self.database = mysqldb.connect(host = host, user = username, 
    passwd = password, db = database)
    self.register = register(self)
  def query(self, query, smart = True):
    if not smart:
      # Not using intelligent query system. Query and return the cursor object.
      cursor = self.database.cursor()
      cursor.execute(query)
      return cursor
    else:
      # Intelligent query system:
      # Execute the query and fetch all of the result rows.
      cursor = self.database.cursor()
      cursor.execute(query)
      rows = cursor.fetchall()
      # Determine the tables fetched from the database
      tables = self.__determine_tables(query)
      # Determine the models used from the tables.
      models = []
      for table in tables:
        models.append(self.__find_model(table))
      result = []
      # Iterate through the result rows.
      for row in rows:
        # Convert the row to a list.
        row = list(row)
        # Reverse the row that the first variable will be returned when 
        # row.pop() is called instead of the last.
        row.reverse()
        # If there was more than one model, return each result row as a list.
        if len(models) > 1: resultobj = []
        # Iterate through the models from the query.
        for model in models:
          # Instantiate a new model.
          m = model()
          # Go through each field in the structure.
          for field in m.structure:
            # Pop of an item from the row.
            item = row.pop()
            m.__setattr__(field.name, field.result(item))
          # If there was more than one model, add the new model class to the 
          # result list.
          if len(models) > 1:
            resultobj.append(m)
          else:
            # Otherwise just use the single model.
            resultobj = m
        # Append the result object (list or model)
        result.append(resultobj)
      # Return the nice ol' result.
      return result
  def close(self):
    self.database.close()
  # -----------------------
  # Private utility methods
  def __determine_tables(self, query):
    """Parse SQL query to determine tables requested."""
    tables = re.findall(r'FROM ([a-z0-9_]+(?: [a-z0-9_]+)?)(, [a-z0-9_]+(?: [a-z0-9_]+)?)*', query)
    processed = []
    for table in tables[0]:
      # Trim whitespace and commas off of something like ", users user".
      table = table.strip(', ')
      # Pull the "users" out of the processed "users user".
      if table.__len__() > 0:
        processed.append(table.split()[0])
      else: continue
    return processed
  def __find_model(self, name):
    """Iterate through the list of models to find one by table name."""
    # Go through tables and see if their table matches the provided one.
    for model in self.models:
      if model.table:
        table = model.table
      else:
        # If no table defined, it tries to extrapolate it from an ideal class
        # name of TableModel (EG: UsersModel)
        table = model.__name__.lower()[:-5]
      if table == name:
        # They match!
        return model
    
# Taken from a tutorial on using the MySQL-Python MySQLdb interface.
"""
    #!/usr/bin/python
    # import MySQL module
    import MySQLdb
    # initialize some variables
    name = ""
    data = []
    # loop and ask for user input
    while (1):
    name = raw_input("Please enter a name (EOF to end): ")
    if name == "EOF":
    break
    species = raw_input("Please enter a species: ")
    # put user input into a tuple
    tuple = (name, species)
    # and append to data[] list
    data.append(tuple)
    # connect
    db = MySQLdb.connect(host="localhost", user="joe", passwd="secret",
    db="db56a")
    # create a cursor
    cursor = db.cursor()
    # dynamically generate SQL statements from data[] list
    cursor.executemany("INSERT INTO animals (name, species) VALUES (%s,
    %s)",
    data)
"""