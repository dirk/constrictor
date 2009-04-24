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
  def filter(self, func):
    # Checks to make sure that the method has not been exposed, since filters
    # should not be exposed.
    if func.__dict__.has_key('Expose') and func.Expose is True:
      raise AttributeError, 'Method cannot be a filter _and_ be exposed at the same time!'
    func.Expose = False
  # Functions that handle the decorators.
  def Before(self, func):
    self.filter(func)
    func.Filter = 'Before'
    func.Priority = 0
    return func
  def After(self, func):
    self.filter(func)
    func.Filter = 'After'
    func.Priority = 0
    return func
  
# Initialize the Filtering class and put it in the namespace as Filter.
Filter = Filtering()

class Controller(object):
  """Represents a controller for processing requests."""
  # Example of using the Before and After filters and exposing methods.
  # * The append() method is used because it's the easiest, clearest, and
  #   simplest way of doing this, and avoids unnecessary abstraction.
  #@Filter.Before
  #def my_before_filter(self):
  #  pass
  #my_before_filter.Priority = 5
  # ^ Optional priority definition, the higher numbered filters are executed first.
  #@Expose
  #def my_exposed_method(self):
  #  pass
  
  # FIXME: Fix this horrible redundancy.
  def before_filters(self):
    filters = []
    for item in dir(self):
      if not item.startswith('__'):
        method = self.__getattribute__(item)
        try:
          if method.Filter is 'Before':
            filters.append(method)
          else: continue
        except AttributeError: continue
      else: continue
    filters.sort(key=lambda obj: (obj.Priority * -1))
    return filters
  
  def after_filters(self):
    filters = []
    for item in dir(self):
      if not item.startswith('__'):
        method = self.__getattribute__(item)
        try:
          if method.Filter is 'After':
            filters.append(method)
          else: continue
        except AttributeError: continue
      else: continue
    filters.sort(key=lambda obj: (obj.Priority * -1))
    return filters