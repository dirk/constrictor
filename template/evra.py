"""
The aim of EValuatedRAttler is to take the ideas of the Rattler templating
system and tie them to Python's eval statement to allow expressions to truly
act like Python expressions.
"""

from __init__ import Template
import re

class EvRa(Template):
  def render(self, data, variables):
    lines = data.split('\n')
    output = ''
    block = None
    scope = variables
    multiline = False
    for line in lines:
      if multiline:
        is_closing = line.find('%>')
        if is_closing is not -1:
          interpret = line[:is_closing].strip()
          line = line[is_closing+2:]
          multiline = False 
        else:
          interpret = line
          line = ''
        exprs = re.split('[^\\];', interpret)
      else:
        items = re.findall(r'(<%=? )(.+?)((?: %>)|(?:$))', line)
        # items looks something like [('<%', "a = 'b'", ' %>')]
        try:
          for item in items:
            if item[2].strip() == '':
              multiline = True
              eval(item[1], scope, globals())
              replace = ''
            elif item[0].strip() == '<%=':
              # Direct output
              #val = self._eval_subexp(item[1], scope)
              val = eval(item[1], scope, globals())
              replace = val
            elif item[0].strip() == '<%':
              """expr = item[1]
              closing = item[2]
              # Test if assignment
              assign = re.split(r'^([A-z0-9\.\[\]]+) *= *(.+)$', expr)
              # ----------
              # Assignment
              if len(assign) is 4:
                # assign looks something like ['', 'a', "'b'", '']
                var = assign[1]
                val = assign[2]
                self._assign_obj_value(var, self._eval_subexp(val, scope), scope)"""
              replaced = re.sub('^[\t ]*', '', item[1])
              exec replaced in globals(), scope
              replace = ''
            else: replace = ''
            original = ''.join(item)
            line = line.replace(original, replace)
        except IndexError:
          pass
      output += line + '\n'
    print output