from evra import EvRa

data = """
test<%b
    
    d = 'test'
    
    e = 'testing3'
    def f():
      return 'testing4'
    %>
<% a = b;b = 'testing2';c = 'data' %>
<%= a %><%= f() %>
"""

t = EvRa()
t.render(data, {
  'a': 'test',
  'b': 'testing'
})