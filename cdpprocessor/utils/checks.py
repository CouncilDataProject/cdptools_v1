CHECK_TYPES_ERR = """
The parameter provided must be one of the following: {p},
Given type: {t}
Given value: {v}
"""

CHECK_TYPES_ERR_FOOTER = """
Allowed types: {p}
Given type: {t}
Given value: {v}
"""

def check_types(var, types, err=CHECK_TYPES_ERR):
    if isinstance(types, list):
        types = tuple(types)

    if not isinstance(types, tuple):
        raise TypeError("""
The "types" parameter provided must be either a list or a tuple.
Given type: {t}
Given value: {v}
""".format(t=type(types), v=types))

    if 'function' in types and callable(var):
        return var

    if isinstance(var, types):
        return var

    err += CHECK_TYPES_ERR_FOOTER
    raise TypeError(err.format(p=types, t=type(var), v=var))
