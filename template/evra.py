"""
The aim of EValuatedRAttler is to take the ideas of the Rattler templating
system and tie them to Python's eval statement to allow expressions to truly
act like Python expressions.
"""

from __init__ import Template
import re, copy

class EV(Template):
  """
  New templating system that replaces EvRa. Continous scan of template instead
  of going line-by-line. 2x performance improvement over EvRa.
  """
  @classmethod
  def csplit(cls, string, pos): return [string[:pos], string[pos:]]
  @classmethod
  def remove_opening_tag(cls, data): return data[2:]
  @classmethod
  def closing_tag_split(cls, data): return data.split(r'%>', 1)
  
  @classmethod
  def render(cls, data, variables):
    scope  = variables
    
    ib = data
    ob = ''
    pos = ib.find(r'<%')
    while pos != -1:
      pre, post = cls.csplit(ib, pos)
      ob += pre
      expr, ib = cls.closing_tag_split(cls.remove_opening_tag(post))
      expr = expr.rstrip() # Remove trailing whitespace
      
      if expr.startswith('='):
        # Take the expression, remove the leading '=' and strip it of any
        # remaing whitespace before evaluating.
        ob += eval(expr[1:].strip(), scope, globals())
      else:
        expr = expr.strip()
        # TODO: Make it easier to have custom block-style statements.
        for_match   = re.match(r'^for (?P<target>\w+) in (?P<items>\w+):$', expr)
        while_match = re.match(r'^while (?P<expr>.+):$', expr)
        if for_match:
          parts = for_match.groupdict()
          block, ib = ib.split('<% end %>', 1)
          collection = eval(parts['items'], scope, globals())
          for item in collection:
            scope[parts['target']] = item
            ob += cls.render(block, scope)
        elif while_match:
          parts = while_match.groupdict()
          block, ib = ib.split('<% end %>', 1)
          while(eval(parts['expr'], scope, globals())):
            ob += cls.render(block, scope)
        else:
          exec expr.strip() in globals(), scope
      pos = ib.find(r'<%')
    ob += ib
    return ob

class EvRa(Template):
  @classmethod
  def render(cls, data, variables):
    lines = data.split('\n')
    # Holds the current namespace
    scope = variables
    scope['end'] = None
    # String to be outputted
    output = ''
    # If it is a block (EG: for, while), this will hold a dictionary with
    # mandatory 'type' key and other keys depending on the type of loop.
    block = None
    
    multiline = False;multiline_indent = 0;multiline_expr = ''
    # Used in the multiline expressions
    cont = True
    # Primary loop, iterating through the lines
    for line in lines:
      # Test to see if it's a for or while loop
      if not multiline and not block:
        # NOTE: For loop has priority over while loop.
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
        else:
          while_loop_items = re.findall(r'(<% while (.+): %>)', line)
          if len(while_loop_items) > 0:
            item = while_loop_items[0]
            item = while_loop_items[0]
            # Grabbing stuff after the <% for... %>
            end = line[(line.find(item[0]) + len(item[0])):]
            # Grabbing stuff before the <% for... %>
            line = line[:line.find(item[0])]
            block = {
              'type': 'while',
              'expr': item[1],
              'content': end + '\n'
            }
      if block:
        # If it is a block, start parsing the block content.
        end_block = False
        pos = line.find(r'<% end %>')
        # If it's still on the first line.
        if end:
          end_pos = end.find(r'<% end %>')
          if end_pos != -1:
            content = end[:end_pos]
            after = end[(end_pos + 9):]
            end_block = True
        elif pos == -1:
          block['content'] += line
          line = ''
        else:
          content = block['content'] + line[:pos]
          after = line[(pos + 9):];line = ''
          end_block = True
        if end_block:
          # Determine block content and either run for or while loop.
          if block['type'] is 'for':
            for item in block['list']:
              scope[block['item']] = item
              line += cls.render(content, scope)
          elif block['type'] is 'while':
            while(eval(block['expr'], scope, globals())):
              line += cls.render(content, scope)
          block = None
          line += after
        end = None
      # Processing multi-line block system.
      if multiline and not block:
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
      # STANDARD PROCESSING SYSTEM
      if cont is True and not block:
        # Match for an expression "<% %>" or an output "<%= %>".
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
    return output