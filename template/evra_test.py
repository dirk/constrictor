from evra import EvRa

data = """
test<%b
    
    d = 'test'
    
    e = 'testing3'
    def f():
      return 'testing4'
    %>
<% a = b;b = 'testing2' %>
<%= a %><%= f() %>
--
<% for item in c: %><%= item %><% end %>test
--
testing2
"""

t = EvRa()
print t.render(data, {
  'a': 'test',
  'b': 'testing',
  'c': [0, 1, 2, 3]
})