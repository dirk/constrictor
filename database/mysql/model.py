class Model(object):
  """
  Base model class.
  """
  ismodel = True
  # Name of the table in the database.
  Table = None
  # Contains a list of the fields in the table.
  Structure = []
  def print_structure(self):
    print self.structure