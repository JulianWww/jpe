import warnings


class jpeWarning(Warning):pass

class jpeDevFuncWarning(jpeWarning):
    " warning raised when function is jut for my benifit and isnt in the doc"
    pass

class jpeClassDataChange(jpeWarning):
    " when a function significantaly changes a class without good reason"
    pass

class jpeRedundantCall(jpeWarning):
    " called when a redundant things are done"
    pass
