from constrictor.middleware import Middleware
from constrictor.utils import forgiving_object

class Smart_Post(Middleware):
  """
  Parses request.post and makes nested objects out of the keys.
  
  NOTE: Not recursive, only goes down one level.
  """
  def pre_method(self, request, params):
    pre = request.post;post = forgiving_object()
    for p in pre:
      parts = [i.strip('.') for i in p.split('.', 2)]
      if len(parts) == 1:
        post.__setattr__(parts[0], pre[p])
      else:
        if not post.__dict__.has_key(parts[0]):
          post.__setattr__(parts[0], forgiving_object())
        post.__getattribute__(parts[0]).__setattr__(parts[1], pre[p])
    request.raw_post = pre;request.post = post