import re

CHECK_TYPES_ERR = """

Allowed types: {p}
Given type: {t}
Given value: {v}
"""

CHECK_STRING_ERR = """

Allowed characters: {a}
Given characters: {g}
"""

def check_types(var, types, err=CHECK_TYPES_ERR):
    """
    Check the provided variable against the provided types given.

    Example:
    ==========
    ```
        >>> temp = "this is a string"
        >>> check_types(temp, str)
        True
        >>> check_types(temp, [str, int])
        True
        >>> check_types(temp, tuple([str, dict]))
        True
        >>> check_types(temp, [int, list, dict])
        TypeError:

        Allowed types: (<class 'int'>, <class 'list'>, <class 'dict'>)
        Given type: <class 'str'>
        Given value: this is a string

        >>> check_types(temp, [int, list, dict], "this message displays first")
        TypeError: this message displays first

        Allowed types: (<class 'int'>, <class 'list'>, <class 'dict'>)
        Given type: <class 'str'>
        Given value: this is a string

    ```

    Parameters
    ==========
    var: object
        Any variable that's type should be checked.
    types: type, list, tuple
        A single type, a list of types, or a tuple of types to check the
        provided variable against.
    err: str
        An additional error message to be displayed before the standard error
        should the provided variable not pass type checks.

    Returns
    ==========
    is_type: bool
        Returns boolean True if the provided variable is of a type given.

    Errors
    ==========
    TypeError:
        The provided variable did not pass type checks.

    """

    # convert to tuple if possible
    if isinstance(types, list):
        types = tuple(types)

    # check types
    if isinstance(var, types):
        return True

    # format error
    if err != CHECK_TYPES_ERR:
        err += CHECK_TYPES_ERR

    # raise error
    raise TypeError(err.format(p=types, t=type(var), v=var))

def check_string(seq, test, err=CHECK_STRING_ERR):
    """
    Check the provided string against the provided regex string.

    Example:
    ==========
    ```
        >>> temp = "sequence"
        >>> check_string(temp, "^[a-zA-Z]+$")
        True
        >>> check_string(temp, "^[A-Z]+$")
        ValueError:

        Allowed characters: ^[A-Z]+$
        Given characters: sequence

        >>> check_string(temp, "^[A-Z]+$", "this message displays first")
        ValueError: this message displays first

        Allowed characters: ^[A-Z]+$
        Given characters: sequence

    ```

    Parameters
    ==========
    seq: str
        The sequence to be checked.
    test: str
        A regex string to be checked against.
    err: str
        An additional error message to be displayed before the standard error
        should the provided sequence not pass regex checks.

    Returns
    ==========
    is_allowed: bool
        Returns boolean True if the provided sequence passes regex string.

    Errors
    ==========
    ValueError:
        The provided sequence did not pass regex checks.
    """

    # enforce types
    check_types(seq, str, "In cdptools.utils.checks.check_string()")
    check_types(test, str, "In cdptools.utils.checks.check_string()")

    # actual check
    if re.match(test, seq):
        return True

    # format error
    if err != CHECK_STRING_ERR:
        err += CHECK_STRING_ERR

    # raise error
    raise ValueError(err.format(a=test, g=seq))
