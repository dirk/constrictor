"""
The aim of EValuatedRAttler is to take the ideas of the Rattler templating
system and tie them to Python's eval statement to allow expressions to truly
act like Python expressions.
"""

from __init__ import Template
import re, copy

class EvRa(Template):
  def render(self, data, variables):
    lines = data.split('\n')
    output = ''
    block = None
    scope = variables
    multiline = False;multiline_indent = 0;multiline_expr = ''
    cont = True
    loop = False
    for line in lines:
      if not multiline and not block:
        # Test to see if it's a for loop
        for_loop_items = re.findall(r'(<% for (\w+) in (\w+): %>)', line)
        if len(for_loop_items) > 0:
          item = for_loop_items[0]
          # Grabbing stuff after the <% for... %>
          end = line[(line.find(item[0]) + len(item[0])):]
          # Grabbing stuff before the <% for... %>
          line = line[:line.find(item[0])]
          block = {
            'type': 'for',
            'list': eval(item[2], scope, globals()),
            'item': item[1],
            'content': end + '\n'
          }
      if block:
        if block['type'] is 'for':
          # Tests if there is an <% end %> in the same line.
          if end and end.find(r'<% end %>') != -1:
            end_pos = end.find(r'<% end %>')
            content = end[:end_pos]
            after = end[(end_pos + 9):]
            custom_scope = copy.copy(scope)
            for item in block['list']:
              custom_scope[block['item']] = item
              line += self.render(content, custom_scope)
            block = None
            line += after
          # Otherwise do normal routine.
          else:
            pos = line.find(r'<% end %>')
            if pos is -1:
              block['content'] += line
              line = ''
            else:
              block['content'] += line[:pos]
              after = line[(pos + 9):]
              line = ''
              custom_scope = copy.copy(scope)
              for item in block['list']:
                custom_scope[block['item']] = item
                line += self.render(block['content'], custom_scope)
              block = None
          # Set end to none to prevent further testing of it for later lines.
          end = None
      if multiline and not block:
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
      if cont is True and not block:
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
            line = line.replace(original + ' %>', str(replace))
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
    #print output
    return output