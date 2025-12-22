import inspect


digits = cols = "123456789"
rows = "ABCDEFGHI"


def raiseNotDefined():
    """Signal that a student / implementer has not provided an implementation.

    This helper raises NotImplementedError rather than exiting the process so
    test harnesses can catch the exception and continue.
    """
    # Look up the caller frame to provide a helpful message.
    caller = inspect.stack()[1]
    fileName = caller.filename
    line = caller.lineno
    method = caller.function
    raise NotImplementedError(f"Method not implemented: {method} at line {line} of {fileName}")


def cross(A, B):
    """Return the cross product (concatenation) of characters/strings in A and B.

    Examples:
      cross('AB', '12') -> ['A1', 'A2', 'B1', 'B2']
      cross(rows, cols) -> ['A1', 'A2', ..., 'I9']
    """
    return [a + b for a in A for b in B]


squares = cross(rows, cols)


# Public API for explicit imports
__all__ = ["digits", "rows", "cols", "squares", "cross", "raiseNotDefined"]