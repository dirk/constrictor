from constrictor.database.mysql import Model, Fields

class User(Model):
  Table = 'auth_users'
  
  id = Fields.Primary()
  username = Fields.String(null = False, length = 32)
  password = Fields.String(null = False, length = 255)
  fullname = Fields.String(null = False, length = 64)
  email = Fields.String(null = False, length = 64)
  last_activity = Fields.Integer(null = False)
  created_at = Fields.Integer(null = False)