import os, sys

def set_path(path):
  """
  This functions sets the path to the directory above the current application 
  to make imports such as 'myapp.models' possible.
  
  * Path should normally be the output from os.getcwd() is the calling file.
  """
  sys.path.append(os.path.join(path, os.pardir))