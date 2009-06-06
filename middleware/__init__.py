from constrictor.utils import forgiving_object

class Middleware(forgiving_object):
  instance = None
  def __init__(self): pass
  def pre_method(self, request, params):
    pass
  def post_method(self, request, params, response):
    pass