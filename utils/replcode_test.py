import replcode
input_text = """
    Normal line.
    Expression <%= 1+2 %>.
    Global variable <%= variable %>.
    
    <%?
        def foo(x):
        	return x+x %>.
    Function <%= foo('abc') %>.
    <%?
    a = [1, 2, 3]
    for b in a:
      OUTPUT(str(b)) %>
    
"""
global_dict = { 'variable': '123' }
output_text = replcode.runPythonCode(input_text,global_dict)
print output_text
