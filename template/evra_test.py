from evra import EvRa

data = """
<% a = b;b = 'testing2';c = 'data' %>
<%= a %><%= c %>
"""

t = EvRa()
t.render(data, {
  'a': 'test',
  'b': 'testing'
})