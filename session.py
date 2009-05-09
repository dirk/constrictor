class Session(object):
  # Stubbing out system for maintaining sessions.
  
  # Points to an iterable object of sessions held somewhere in the memory.
  sessions = None
  
  # NOTE: Cookie time formatting: time.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
  """
  session = {
    'id': # md5 hash of random integer and system time.
    'user_agent': # Actual user-agent, combined with id for verification.
    'ip_address'
    'data': {}
  }
  """
  def __init__(self, sessions_object = None):
    self.sessions = sessions_object
  def retrieve(self, request):
    # Processes a request, grabs session ID, and then retrieves the object
    # from Session.sessions.
    print request
  def create(self, request, session):
    # Establish a new session, adds headers to the passed Request object.
    pass
  def destroy(self, request, session):
    # Opposite of Session.create.
    pass