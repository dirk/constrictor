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
<% test = 0 %>
<% while test < 10: %><% test += 1 %><%= test %><% end %>
"""

t = EvRa()
def test():
  t.render(data, {
    'a': 'test',
    'b': 'testing',
    'c': [0, 1, 2, 3]
  })

#import cProfile, pstats
#cProfile.run('test()', 'stats')
#p = pstats.Stats('stats')
#p.strip_dirs().sort_stats('cumulative').print_stats(10)


if __name__ == '__main__':
  import profile
  import evra
  
  benchmark_template = """
  <% b = " rules" %>
  <%= a + b %>
  <% for i in items: %>
    <%= i %>
  <% end %>
  """
  benchmark_data = {
    'a': 'Dirk',
    'items': (', ', 'and', ' you ', 'know it.')
  }
  
  def benchmark_evra():
    for i in range(1000):
      evra.EvRa.render(benchmark_template, benchmark_data)
  def benchmark_ev():
    for i in range(1000):
      evra.EV.render(benchmark_template, benchmark_data)
  import cProfile, pstats
  cProfile.run('benchmark_evra()', 'stats')
  p = pstats.Stats('stats')
  p.strip_dirs().sort_stats('cumulative').print_stats(10)
  import cProfile, pstats
  cProfile.run('benchmark_ev()', 'stats')
  p = pstats.Stats('stats')
  p.strip_dirs().sort_stats('cumulative').print_stats(10)