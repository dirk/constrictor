from constrictor.core import *

from models import *

class Users(Controller):
  def index(self, request, params):
    return 'a list of users'
  def login(self, request, params):
    return 'a login screen'
  @Filter.Before
  def _is_authenticated(self, request, params):
    if not request.session.user and request.method != self.login:
      return request.redirect('/auth/users/login')
