"""all General Errors

a module containing the general jpe errors"""

class jpeError(Exception):
    "std Error type"
    pass

class calculationError(jpeError):
    "a function call has a calculation error"
    pass

class modeError(jpeError):
    """when a function or operation has multiple modes this error is caled if an invalid mode was passed"""
    pass
