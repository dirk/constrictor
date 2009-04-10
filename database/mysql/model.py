class model(object):
  """
  Base model class.
  """
  # Name of the table in the database.
  table = None
  # Contains a list of the fields in the table.
  structure = []
  def print_structure(self):
    print self.structure