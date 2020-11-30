import math
import warnings
import jpe.errors

def testF(x):
    return x**2
def testdf(x):
    return 2*x

def neuton(fun, dfun, val=0, acc=5, start=None, maxIter=1_000_000, warn=False):
    """
    neuton algorythem
    fun is the function ur scanning
    dfun is the derivative of fun
    fun or dfun can be funcons or string if stirngs neuton will crete lambda x: fun bzw dfun
    string val is the value that we want at the end fun(res) = val
    int acc is the amoutn of post 0 digits in result,
    float start is the starting location for the scan if none it will default to val
    int maxIter is the max aount of iterations before force end defaults to 1 mil
    bool warn will raise waring if max iter ending
    """
    #initiate variables for x, f and df
    #code appears self explanatory plz complain if it sint
    x = val if start is None else start
    # if fun ist str init function and save under f else make f equal to fun
    if isinstance(fun, str): f = lambda x: eval(fun)
    else: f = fun
    # if dfun ist str init function and save under df else make df equal to dfun
    if isinstance(dfun, str): df = lambda x: eval(dfun)
    else: df = dfun
    # accDelta is the change of the derivative at witch we stop
    accDelta = 10**(-acc-1)
    # for i in range(maxIter) but this has mamory problems as 1 mil is a little large
    iterCounter = 0
    while iterCounter < maxIter:
        iterCounter += 1
        # calculate delta from df and dx 
        delta = (f(x)-val)/df(x)
        x -= delta
        # if delte is less than 1/10**acc end loop
        if delta < accDelta:
            return round(x, acc)
    # raise calc abbort warning
    if warn:
        warnings.warn(jpe.errors.jpeCalculationAbortedWarning(f"abborted calculations du to to max iter rate reached last delta is {delta}"))
    return round(x, acc)
    
