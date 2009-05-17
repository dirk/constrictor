from Cookie import SimpleCookie
import time
from string import letters, digits
from random import choice

class Session(object):
  id = int
  user_agent = str
  ip_address = str
  last_activity = int
  def __init__(self, id, user_agent, ip_address):
    self.id = id;self.user_agent = user_agent;self.ip_address = ip_address
    self.last_activity = int(time.time())
class SessionStore(object):
  # Stubbing out system for maintaining sessions.
  
  # Points to an iterable object of sessions held somewhere in the memory.
  sessions = []
  
  # NOTE: Cookie time formatting: time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime())
  """
  session = {
    'id': # md5 hash of random integer and system time.
    'user_agent': # Actual user-agent, combined with id for verification.
    'ip_address',
    'last_activity'
    'data': {}
  }
  """
  def __init__(self, instance, sessions_object = None):
    self.instance = instance
    self.sessions = sessions_object or []
  def retrieve(self, request):
    """
    Processes a request, grabs session ID, and then retrieves the object
    from Session.sessions.
    
    Returns None if it cannot retrieve a session.
    """
    try:
      cookie_data = request.request_headers['cookie']
      cookie = SimpleCookie(cookie_data)
      # Make sure session is set
      if not cookie.has_key('session_id'): return None
      # Find the session by the provided session_id.
      # Checks against user_agent and ip_address headers for extra security.
      for session in self.sessions:
        if session.id == cookie['session_id'].value and \
          session.user_agent == request.user_agent and \
          session.ip_address == request.ip_address:
            session.last_activity = int(time.time())
            return session
    except KeyError: return None
  def create(self, request, auto_header = True, session_id = None):
    """
    Establish a new session. Returns generated Session object.
    
    Will not add headers to the passed Request object if auto_header is False.
    """
    if request.session: return request.session
    if not session_id:
      chars = letters + digits
      # Generate random alpha-numeric string.
      random_string = ''
      for i in range(32):
        random_string += choice(chars)
      session_id = random_string
    # Initialize and return the Session with either the provided session_id or
    # a generated one.
    session = Session(session_id, request.user_agent, request.ip_address)
    # If it is set, put into the headers of the Request to be sent to the
    # browser.
    if auto_header:
      request.headers.append(self.get_headers(request, session))
    return session
  def get_headers(self, request, session, expire_offset = 1209600):
    # NOTE: 1209600 is two weeks in seconds
    cookie = SimpleCookie()
    cookie['session_id'] = session.id
    expire_time = time.gmtime(time.time() + expire_offset)
    expire = time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', expire_time)
    cookie['session_id']['expires'] = expire
    cookie['session_id']['path'] = '/'
    cookie['session_id']['domain'] = request.server_instance.domain
    return cookie.output()
  def destroy(self, request, session):
    # Opposite of Session.create.
    pass