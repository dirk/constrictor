VERSION = (0, 5, 1, 'Beta')
# Pretty representation of the version.
VERSION_STRING = '.'.join([str(x) for x in VERSION[:3]])

if __file__.endswith('.pyc'):
  PATH = __file__[:-12]
else:
  PATH = __file__[:-11]