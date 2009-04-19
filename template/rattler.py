# Rattler is the new templating system for Constrictor.
# It will hopefully end up replacing the repl library.

from __init__ import Template
import re

class Rattler(Template):
  def render(self, data, variables):
    lines = data.split('\n')
    #print re.findall(r'<% (.+?) %>', data)
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
        exprs = re.split(r'[^\\];', interpret)
        for expr in exprs:
          assign = re.split(r'^([A-z0-9\.\[\]]+) *= *(.+)$', expr)
          # ----------
          # Assignment
          if len(assign) is 4:
            # assign looks something like ['', 'a', "'b'", '']
            var = assign[1]
            val = assign[2]
            self._assign_obj_value(var, self._eval_subexp(val, scope), scope)
      if not multiline:
        items = re.findall(r'(<%=? )(.+?)((?: %>)|(?:$))', line)
        # items looks something like [('<%', "a = 'b'", ' %>')]
        try:
          for item in items:
            if item[2].strip() == '':
              multiline = True
              exprs = re.split(r'[^\\];', item[1])
              for expr in exprs:
                assign = re.split(r'^([A-z0-9\.\[\]]+) *= *(.+)$', expr)
                # ----------
                # Assignment
                if len(assign) is 4:
                  # assign looks something like ['', 'a', "'b'", '']
                  var = assign[1]
                  val = assign[2]
                  self._assign_obj_value(var, self._eval_subexp(val, scope), scope)
              replace = ''
            elif item[0].strip() == '<%=':
              # Direct output
              val = self._eval_subexp(item[1], scope)
              replace = val
            elif item[0].strip() == '<%':
              expr = item[1]
              closing = item[2]
              # Test if assignment
              assign = re.split(r'^([A-z0-9\.\[\]]+) *= *(.+)$', expr)
              # ----------
              # Assignment
              if len(assign) is 4:
                # assign looks something like ['', 'a', "'b'", '']
                var = assign[1]
                val = assign[2]
                self._assign_obj_value(var, self._eval_subexp(val, scope), scope)
              replace = ''
            else: replace = ''
            original = ''.join(item)
            line = line.replace(original, replace)
        except IndexError:
          pass
      output += line + '\n'
    print output
  def _eval_subexp(self, subexp, scope):
    """
    Evaluates a sub-expression for both string concatenation and
    mathematical expressions.
    """
    items = re.split(r' ?([+*]) ?', subexp.strip())
    
    previous = None
    operator = None
    counter = 0
    while counter < len(items):
      item = items[counter]
      if item is '+' or item is '*':
        operator = item
      else:
        # is_function
        if self._is_function(item):
          obj, first = item.split('(', 1)
          subitems = ''
          if first.endswith(')'):
            subitems += first[:-1]
          else:
            subitems += first
            skip = 0
            for subitem in items[counter+1:]:
              skip += 1
              if not subitem.endswith(')'):
                subitems += subitem
              else:
                subitems += subitem[:-1]
                counter += skip
                break
          subexps = re.split(r' ?, ?', subitems)
          call_args = []
          for sub in subexps:
            call_args.append(self._eval_subexp(sub, scope))
          func = self._lookup_obj_value(obj, scope)
          return func(*call_args)
        elif not item.endswith(')'):
          value = self._eval_subitem(item, scope)
          #print value
          try:
            if previous is None: previous = value
            if operator is '+':
              previous = previous + value
            elif operator is '*':
              previous = previous * value
          except TypeError:
            raise TypeError, 'Cannot perform addition/multiplication on type'
          #print item
      counter += 1
    return previous
  def _eval_subitem(self, item, scope):
    if self._is_string(item):
      return str(item[1:-1])
    if item.isdigit():
      return int(item)
    if self._is_obj(item):
      return self._lookup_obj_value(item, scope)
  def _is_string(self, item):
    if item.startswith('"') and item.endswith('"'):
      return True
    elif item.startswith("'") and item.endswith("'"):
      return True
    else: return False
  def _is_function(self, item):
    return re.findall(r'^([A-z0-9\.\[\]]+)\(', item)
  def _is_obj(self, item):
    return re.findall(r'^([A-z0-9\.\[\]]+)$', item)
  def _lookup_obj_value(self, item, scope):
    item = re.sub(r'(?P<name>[A-z0-9]+)\[(?P<value>.+)\]', r'\g<name>.[\g<value>]', item)
    parts = item.split('.', 1)
    if len(parts) is 1:
      return scope[item]
    elif parts[1].startswith('['):
      return eval("scope['" + parts[0] + "']" + parts[1])
    else:
      return eval("scope['" + parts[0] + "']." + parts[1])
  def _assign_obj_value(self, var, val, scope):
    scope[var] = val