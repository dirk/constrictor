VERSION = (0, 3, 0, 'Alpha')
# Pretty representation of the version.
VERSION_STRING = '.'.join([str(x) for x in VERSION[:3]])

if __file__.endswith('.pyc'):
  PATH = __file__[:-12]
else:
  PATH = __file__[:-11]