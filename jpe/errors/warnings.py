"all the important warnings in jpe"

import warnings


class jpeWarning(Warning):
    "jpe warning base class"
    pass

class jpeDevFuncWarning(jpeWarning):
    " warning raised when function is jut for my benifit and isnt in the doc"
    pass

class jpeClassDataChange(jpeWarning):
    " when a function significantaly changes a class without good reason"
    pass

class jpeRedundantCall(jpeWarning):
    " called when a redundant things are done"
    pass

class jpeCalculationAbortedWarning(jpeWarning):
    """called when an algorythem ends calculations becuse of iteration lim rech
    
    is mostly called by framework.algorythems"""
    pass
