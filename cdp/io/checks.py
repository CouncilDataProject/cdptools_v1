CHECK_STRING_ERR = """
The parameter provided needs to be a string.
Given: {s_type}
Please view our documentation for an example.
"""

CHECK_FUNCTION_ERR = """
The parameter provided needs to be a function.
Given: {f_type}
Please view our documentation for an example.
"""

def check_string(s, err=CHECK_STRING_ERR):
    if isinstance(s, str):
        return s
    else:
        raise TypeError(err.format(s_type=type(s)))

def check_function(f, err=CHECK_FUNCTION_ERR):
    if callable(f):
        return f
    else:
        raise TypeError(err.format(f_type=type(f)))
