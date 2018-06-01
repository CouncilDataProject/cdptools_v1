CHECK_TYPES_ERR = """
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

    if err != CHECK_TYPES_ERR:
        err += CHECK_TYPES_ERR_FOOTER

    raise TypeError(err.format(p=types, t=type(var), v=var))
