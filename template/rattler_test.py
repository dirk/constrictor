from rattler import Rattler

data = """
<% a = 'b' %><% b.d = 'test' + c.d('test' + 'b', 'testing' + 'c') + e(2 * 2) + f.g(2 * 2) + g.f %>
<% array[0] %>
<%= a %>
<% for a in b:
test %>
"""
data2 = """
<% b = 2 * 2 * d + array[1].g %>
<% c = f(f('test'))
d = 'test'
e = 'test' %>
<% c = 'test' %>
<%= c * b %>
<%= d %>
"""

class testclass(object):
  f = 'test'
  g = 10
def func(val):
  a = list(val)
  a.reverse()
  return ''.join(a)
r = Rattler()
r.render(data2, {
  'g': testclass(),
  'array': [10, testclass()],
  'd': 5,
  'f': func
})