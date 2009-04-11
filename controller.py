class Controller(object):
  """Represents a controller for processing requests."""
  # Filters
  Before = []
  After = []
  # Methods to be exposed to the routing system.
  # NOTE: This is to prevent methods that aren't supposed to be able to be
  #       called from being called through wild-card method-name-based
  #       routing systems.
  Methods = []
  # Example of using the Before and After filters and exposing methods.
  # * The append() method is used because it's the easiest, clearest, and
  #   simplest way of doing this, and avoids unnecessary abstraction.
  #@Before.append
  #def my_before_filter(self):
  #  pass