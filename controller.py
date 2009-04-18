def Expose(func):
  """
  This is to prevent methods that aren't supposed to be able to be
  called from being called through wild-card method-name-based
  routing systems.
  """
  # Checks to make sure that the method has not been previously prevented from
  # being exposed (Currently only a Filter would do this).
  if func.__dict__.has_key('Expose') and func.Expose is False:
    raise AttributeError, 'Method cannot be exposed _and_ be a filter at the same time!'
  func.Expose = True
  return func
class Filtering(object):
  """
  Class for setting functions of controllers to be filters.
  
  Priority defines their sort order. Filters are sorted by priority (With 0
  being the lowest priority) and then alphabetically (With "A" coming first).
  """
  def __init__(self):
    self.Before.filter = self.filter
    self.After.filter = self.filter
  def filter(self, func):
    # Checks to make sure that the method has not been exposed, since filters
    # should not be exposed.
    if func.__dict__.has_key('Expose') and func.Expose is True:
      raise AttributeError, 'Method cannot be a filter _and_ be exposed at the same time!'
    func.Expose = False
  # Classes that handle the decorators.
  class Before(object):
    def __init__(self, obj):
      # It was called like "@Filter.Before" and the obj is the function.
      if type(obj) is not int:
        self.filter(self)
        self.Filter = {'Type': 'Before','Priority': 0}
      # It was called like "@Filter.Before(x) and the obj is the priority."
      else:
        self.priority = obj
    def __call__(self, func):
      self.filter(func)
      func.Filter = {'Type': 'Before','Priority': self.priority}
      return func
  class After(object):
    def __init__(self, obj):
      # It was called like "@Filter.After" and the obj is the function.
      if type(obj) is not int:
        self.filter(self)
        self.Filter = {'Type': 'After','Priority': 0}
      # It was called like "@Filter.After(x) and the obj is the priority."
      else:
        self.priority = obj
    def __call__(self, func):
      self.filter(func)
      func.Filter = {'Type': 'Before','Priority': self.priority}
      return func
  
# Initialize the Filtering class and put it in the namespace as Filter.
Filter = Filtering()

class Controller(object):
  """Represents a controller for processing requests."""
  # Example of using the Before and After filters and exposing methods.
  # * The append() method is used because it's the easiest, clearest, and
  #   simplest way of doing this, and avoids unnecessary abstraction.
  #@Fitler.Before(priority)
  #def my_before_filter(self):
  #  pass
  #@Expose
  #def my_exposed_method(self):
  #  pass
  def before_filters(self):
    for item in dir(self):
      if not item.startswith('__'):
        method = self.__getattribute__(item)
        try:
          if method.Filter['Type'] is 'Before':
            print method
          else: continue
        except AttributeError: continue
      else: continue