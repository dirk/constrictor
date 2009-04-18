from __init__ import Template
from constrictor.utils import replcode

class repl(Template):
  def render(self, data, variables):
    return replcode.runPythonCode(data, variables)