"""
MySQL backend API for Constrictor. Contains the revolutionary Model-Query 
systems.

~ Written by Dirk in the early days of Constrictor, left for posterity.
"""
# Import Python modules.
import re
# Import mysqldb module. (Must install yourself, not included with Python.)
import MySQLdb as mysqldb

# Register utility to be bound into the database. Allows for something like 
# mysql.register.model or mysql.register.query.
from register import register
# Auto-importing fields to make stuff easier.
import fields as Fields
# Base model class.
from model import Model
from query import Query

class mysql(object):
  database = None
  models = []
  queries = []
  def __init__(self, *auto_connect):
    """
    Optional four arguments (host, username, password, database) are passed
    to mysql.connect. Allows for auto-connect functionality for less LOC in a
    single-file application.
    """
    # Establish database connection
    self.register = register(self)
    Query.mysql = self
    Model.mysql = self
    # Only connect if passed 4 parameters
    # TODO: Add more connection options for greater flexibility.
    if len(auto_connect) is 4: self.connect(*auto_connect)
  def connect(self, host, username, password, database):
    "Takes connection parameters and establishes a MySQLdb connection."
    self.database = mysqldb.connect(host = host, user = username, 
    passwd = password, db = database)
  def generate_create(self, model):
    base = "CREATE TABLE `%s` (" % model.Table
    primary = ''
    for f in model.Structure:
      base += '\n\t`%s` %s,' % (f.name, f.generate())
      if type(f) is Fields.Primary:
        primary = '\n\tPRIMARY KEY (`%s`)' % f.name
    base += primary + '\n);'
    return base
  def close(self):
    self.database.close()
  def get_model(self, identifier):
    """
    Tries as hard as it can to get the model from either a model or string.
    Looks in mysql.models if it isn't a model.
    
    Please note, the matching is not case-specific.
    """
    try:
      if identifier.ismodel: return identifier
    except: pass
    for model in self.models:
      if model.Table.lower() == identifier.lower() or \
        model.__name__.lower()[:-5] == identifier.lower():
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