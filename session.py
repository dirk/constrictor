from Cookie import SimpleCookie

class Session(object):
  # Stubbing out system for maintaining sessions.
  
  # Points to an iterable object of sessions held somewhere in the memory.
  sessions = []
  
  # NOTE: Cookie time formatting: time.strftime('%a, %d-%b-%Y %H:%M:%S GMT', time.gmtime())
  """
  session = {
    'id': # md5 hash of random integer and system time.
    'user_agent': # Actual user-agent, combined with id for verification.
    'ip_address'
    'data': {}
  }
  """
  def __init__(self, sessions_object = None):
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
      # TODO: Add user_agent and IP address checks for security!
      for session in self.sessions:
        if session['id'] == cookie['session_id'].value:
          return session
    except KeyError: return None
  def create(self, request, session):
    # Establish a new session, adds headers to the passed Request object.
    pass
  def destroy(self, request, session):
    # Opposite of Session.create.
    pass