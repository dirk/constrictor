from constrictor.utils import forgiving_object

class Middleware(forgiving_object):
  instance = None
  def pre_method(self, request, params):
    pass