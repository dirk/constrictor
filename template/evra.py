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
    multiline = False;multiline_indent = 0;multiline_expr = ''
    cont = True
    for line in lines:
      if multiline:
        # Processing multi-line block system.
        is_closing = line.find('%>')
        if is_closing is -1:
          multiline_expr += line[multiline_indent:] + '\n'
          # cont: Tells the standard processing system whether to proceed or
          #       not. Will be True for the last line of the block.
          cont = False
          line = ''
        else:
          multiline_expr += line[multiline_indent:(is_closing - 1)]
          #print multiline_expr.__repr__()
          exec multiline_expr in globals(), scope
          line = line[(is_closing + 3):]
          multiline = False;multiline_indent = 0
          cont = True
      if cont is True:
        # STANDARD PROCESSING SYSTEM
        # Match for an expression or an output.
        items = re.findall(r'(<%=? )(.+?) %>', line)
        # items looks something like [('<%', "a = 'b'", ' %>')]
        try:
          for item in items:
            if item[0].strip() == '<%=':
              # Direct output
              val = eval(item[1], scope, globals())
              replace = val
            elif item[0].strip() == '<%':
              # Execute an expression
              #replaced = re.sub('^[\t ]*', '', item[1])
              exec item[1] in globals(), scope
              replace = ''
            
            original = ''.join(item)
            line = line.replace(original + ' %>', replace)
        except IndexError:
          pass
        line += '\n'
      # Detect if it's a block statement and initiate multi-line block system.
      pos = line.find(r'<%b')
      if pos is not -1:
        multiline = True
        multiline_indent = pos
        multiline_expr = line[(pos + 4):]
        line = line[:pos]
      output += line
    print output