from __future__ import division
import warnings
import jpe.errors
import math, time, random

inf = float("inf")
"""infinity

a floating point number with value infinity"""

_eps = 1.4902e-08
"""epsilon value

the epsilon for the brent algorythem
"""
_golden = 0.381966011250105097
"""golden mean

the golden mean used for the brent algorythem
"""


class modes:
    """operation modes

    a read only class contining the modes for the search algorythems
    not all modes wok with all search functions this will be specified in the function invalid modese will raise errors
    minimum: the algorythem will search for the min value of the function its given according to ist owne parameters
    maximum: same as minimum just max rather than minimum
    equalVal: will look for the minimum diference betwean the function and the value given to the seach algorythems
    """
    minimum = 1
    "find the minimum value of the function"
    maximum = 2
    "find the maximum value of the function"
    equalVal = 3
    "find the value of the function where f(x)=the value passed to the function as val"

def testF(x):
    """demo function
    
    @param x: the value to scan for
    @type x: float"""
    return x**2
def testdf(x):
    """derivative of demo function
    
    @param x: the value to scan for
    @type x: float
    """
    return 2*x

functionType = type(lambda x: x)
"""type of function

the datatye for functions, basikly it is used to scheck weather a variable contains a function
"""

def neuton(fun, dfun, val=0, acc=5, start=None, maxIter=1_000_000, warn=False):
    """seaks the position of a functon sothat the fun(result) = val where result is the output of this function using neuton algroythem

    give it a function fun and its derivative dfun, as well as a value val
    at each step in the convergence it will substract (f(x)-val)/df(x) from x
    it will do this untill (f(x)-val)/df(x) is less than 1/10**acc or maxIter is reached
    if maxIter is reached and warn is True it will complain about not finding a solution
    it will than return a rounded version of the result

    @param fun: the function the the algorythem runs on to find the result as described above
                is string function will be built as lambda x: eval(fun)
    @type fun: string or function

    @param dfun:   the derivative of fun
                   is string function will be built as lambda x: eval(dfun)
    @type dfun: function or string

    @param val: the value the function must have at the end
                defaults to 0
    @type val: float optional

    @type acc:    int otional
    @param acc:   the accuracy at witch the calculations stop in post comma digits

    @type start:  function, float optional
    @param start: the starting value of the algorythem
                  if float the starting value will be start
                  if function it will run the function with parameter val and use the result witch must be a float, int, jfloat etc
    @type maxIter:int
    @param maxIter: maximum amount of iterations allowed before function terminates and maybe raises warnings
    @type warn:   bool
    @param warn:        weather or not to raise a warning when code teminates du to max Iters reached

    @return: float
            best approximation found for func(result) = val
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

def intervallHalving(fun, val=0, acc=10, top=None, bottom=None, max_Iter=1_000_00, warn=False):
    """
    seaks the position of a functon sothat the fun(result) = val where result is the output of this function using the bisection algroythem

    input a function and a avalu it shuld search as well as some definition of the search intervall contining a solution
    and it will return an approximation of that solution by halving the intervall betwean the values and finding out in witch set the solution is locatd

    IMPORTANT: there must be a solution in [bottom:top] (or [top:bottom]) or a jpeCalculationError is raised

    @type func:   function or string
    @param func:       the function we are checking against
            if string function will be lambda x: eval(func)
            this function must be continous
            
    @type val:    float
    @param val:        the value the function must have at the end
            defaults to 0
            
    @type acc:    int
    @param acc:        the amount of postcomma digits we want to calculate to

    @type top:    float or function optional
    @param top:     the top of the section we are checking
                    if ist a function the programm will use the result of that function as an input for top run parameters are(val)
                    default is val aka if top is None the input will be val

    @type bottom: float optional
    @param bottom:        the bottom of the secton we are checking
                    if ist a function the programm will use the result of that function as an input for top run parameters are(val)
                    default is val aka if top is None the input will be -val

    @type max_Iters: int
    @param max_Iters: the maximum amount of iterations
    @type warn:   bool
    @param warn:        weather to raise warnings

    @return: float
            best approximation for x so that fun(x) = val
    
    """
    # just run the subscript
    return _intervallHalving(fun, val, acc, top, bottom, max_Iter, warn)


def monteCarloBisektion(fun, val=0, acc=10, top=None, bottom=None, max_Iter=1_000_00, warn=True, seed=None, sigma=None):
    """
    seaks the position of a functon so that the fun(result) = val where result is the output of this function using the bisection algroythem with random elements

    input a function and a avalu it shuld search as well as some definition of the search intervall contining a solution
    and it will return an approximation of that solution by spliting the intervall into random sizes and than finding out in witch set the solution is locatd

    IMPORTANT: there must be a solution in [bottom:top] (or [top:bottom]) or a jpeCalculationError is raised

    @type func:   function or string
    @param func:       the function we are checking against
            if string function will be lambda x: eval(func)
            this function must be continous
            
    @type val:    float
    @param val:        the value the function must have at the end
            defaults to 0
            
    @type acc:    int
    @param acc:        the amount of postcomma digits we want to calculate to

    @type top:    float or function optional
    @param top:     the top of the section we are checking
                    if ist a function the programm will use the result of that function as an input for top run parameters are(val)
                    default is val aka if top is None the input will be val

    @type bottom: float optional
    @param bottom:        the bottom of the secton we are checking
                    if ist a function the programm will use the result of that function as an input for top run parameters are(val)
                    default is val aka if top is None the input will be -val

    @type max_Iters: int optionoal
    @param max_Iters: the maximum amount of iterations
    @type warn:   bool optional
    @param warn:        weather to raise warnings

    @param seed: seed for randomness defaults to time.time()
    @type seed: int or None optional

    @param sigma: sigma for guassean random if not None will use guassean else linear random distiribution
    @type sigma: float or None optional

    @return: float
            best approximation for x so that fun(x) = val
    
    """
    # just run subscript the True sais that it uses Montecarlo
    return _intervallHalving(fun, val, acc, top, bottom, max_Iter, warn, 1, seed)

def _intervallHalving(fun, val, acc=10, top=None, bottom=None, max_Iter=1_000_00, warn=True, runAsMontecarlo=0, seed=None, sigma=1):
    """
    intervall halving algorythem so that fun(result)=val, top and bottom is the top (bottom respectivly) value defaults to val but can alsow be a func taking val as a parameter

    max_Iter is the maximum iteration number
    warn if func should raise warnings
    """
    initTop, initBottom = top, bottom

    # initiate boundry values
    #if top or bottom are functions set topVal, bottomval to result of funcon else set to val or -val repectivly or the values given 
    topVal = top(val) if isinstance(top, functionType) else top if top!=None else val
    bottomVal = bottom if isinstance(bottom, functionType) else bottom if bottom!=None else -val
    #create lambda for center value calculation
    if runAsMontecarlo==0:
        getMidVal = lambda : (topVal + bottomVal)/2
    # if we run as std montecarlo
    elif runAsMontecarlo==1 and sigma is None:
        getMidVal = lambda : bottomVal + random.random()*(topVal-bottomVal)
    # if we use guassean to that
    elif runAsMontecarlo==1:
        getMidVal = lambda : bottomVal + max(min(random.gauss(.5, sigma),1),0)*(topVal-bottomVal)
    else:
        raise ValueError("no valid operation mode found plz dont call this function directly")
    # set the random seed
    random.seed(time.time() if seed is None else seed)
    # if we run this algorythem as montecarlo 
    midVal = getMidVal()
    #crate lambda to find out if the value is in the a certain area asuming its a continuous function is not 100 percent reliable
    isInInterval = lambda edge1, edge2: fun(edge1) <= val <= fun(edge2) or fun(edge1) >= val >= fun(edge2)
    #initiate value vector
    #element 0 is fun(bottomVal), element 1 is fun((bottomVal+topVal)/2) and element 3 is fun(topVal)
    yValues = [fun(bottomVal), fun(midVal), fun(topVal)]

    # crate acc delta var accDelta = 1/10**acc
    accDelta = 10**(-acc)
    
    # for i in range(maxIter) but this has mamory problems as 1 mil is a little large
    iterCounter = 0
    while iterCounter < max_Iter:
        iterCounter += 1
        # schrink the interval
        if isInInterval(topVal, midVal):
            # if the solution is between top and mid set interval to that
            bottomVal = midVal
            midVal = getMidVal()
            yValues[0] = yValues[1]
            yValues[1] = fun(midVal)
            
        elif isInInterval(bottomVal, midVal):
            # else to the same just with the other half of the intervall
            topVal = midVal
            midVal = getMidVal()
            yValues[2] = yValues[1]
            yValues[1] = fun(midVal)

        else:
            # if its not in the interval something went wrong
            raise jpe.errors.calculationError(f"solution not in intervall according to aproximation if you think it schuld be plz file a bug report, the bounds of the intervall are {topVal} and {bottomVal}, ty ajustin input interval of size {initTop} :{initBottom}")
        #if the interval size is less than acc nothing will change in the values we care about so calculations end
        if abs(topVal-bottomVal) < accDelta:
            return round(midVal, acc)
    # warn if termination du to iter count reach
    if warn:
        warnings.warn(jpe.errors.jpeCalculationAbortedWarning(f"calculations abborted for value intervall Having algorythem du to max iters reached, interval is [{bottomVal}:{topVal}]"))
    return round(midVal, acc)

def regulaFalsi(func, val=0, x1=None, x2=None, acc=10, maxIter=500, warn=False):
    """
    estimates a solution for func(result) = val where result is the result of these function using regulaFalsi algorythem

    will find 0 locations of a function by tracing a line (l) throw points (x1, func(x1)) and (x2, func(x2)) and than find the intersect
    of l and the x axis the interect is a point with coordinates (i, 0) than set x1 to x2 and x2, to i do this untill accurac is reaced or
    we run out of iteration length


    @type func:   function or string
    @param func:  the function checked against
                  if func is a string the code generates a function of type lambda x: eval(func)

    @type val:    float
    @param val:   the value we want to check func for

    @type x1:     float optional
    @param x1:    the xpos of the first point of the ray

    @type x2:     float optional
    @param x2:    the xpos of the second point of the ray

    @type acc:    int optional
    @param acc:   numper of post comma digits to calculate for

    @type maxIter:  int
    @param maxIter: maximum number of iterations before abbort

    @type warn:   bool
    @param warn:  if true we raise warning if abborted by max iters

    @return: float
             best approximation for x so that fun(x) = val

    """    
    # if str input generat fun function from string
    if isinstance(func, str): fun = lambda x: eval(func)
    else: fun =func
    # generate get value function to make getValue(fun(result)) = 0
    getValue = lambda x: fun(x) - val
    # crate recursion function x1, x2 are the positions to scan| y1, y2 are the values of getValue at x1, x2, acc the search acuracy, and iter the iteration counter
    def recScript(x1, x2, y1, y2, acc, iteration):
        #caluclate new value intersect 
        new_x = x1 - (x2-x1)/(y2-y1)*y1
        # get the y value for the iteratior
        new_y = getValue(new_x)
        # if done iterating or acc reached return result
        if iteration == 0 or abs(x1-x2) < acc:
            # if end du to iter lim reach and war is true raise a warning
            if iteration == 0 and warn:
                warnings.warn(jpe.errors.jpeCalculationAbortedWarning("rec limite reached without acc being reached error is {abs(x1-x2)}"))
            return new_x
        # go for recursion making x1 be old x2  and x2 be new_x same for y
        return recScript(x2, new_x, y2, new_y, acc, iteration-1)
    # initiate val_1, val_2 to x1, x2 unless tey are function in witch case set to funcon return value with para val
    val_1 = x1(val) if isinstance(x1, functionType) else x1
    val_2 = x2(val) if isinstance(x2, functionType) else x2
    
    # runn the recursion script see above   and round value to acc
    return round(recScript(val_1, val_2, getValue(val_1), getValue(val_2), 10**(-acc), maxIter), acc)

def halley(func, dfunc, ddfunc, val=0, init_x=None, acc=10, maxIter=1_000_000, warn=False):
    """estimates a solution for func(result) = val where result is the result of these function using halley algorythem
    
    given a function func, its derivative dfunc and the second derivative ddfunc we can
    find a solution for func(result) = val, we are looking for result to do this we use a similar aproche to the neuton algorythem
    except that conversion calculation is (2*func(x)*dfunc(x))/(2*dfunc(x)**2-func(x)*ddfunc(x)) rather than what is used by neuton

    @type func:   function, string
    @param func:  function we want to check agrainst
                  if func is a string function is generated as lambda x: eval(func)

    @type dfunc:  function, string
    @param dfunc: derivative of the function we want to check agrainst
                  if dfunc is a string function is generated as lambda x: eval(dfunc)

    @type ddfunc: function, string
    @param ddfunc:second derivative of the function we want to check agrainst
                  if ddfunc is a string function is generated as lambda x: eval(ddfunc)

    @type val:    float
    @param val:   the value we want func(result) to have at the end

    @type init_x: float
    @param init_x:initial guess for the result

    @type acc:    int
    @param acc:   number of post comma digits

    @type maxIter:int
    @param maxIter:maximum number of iterations before abbort

    @type warn:   bool
    @param warn:  if true a warning is raised when max iter is reached


    @return: float
             the result ot the calculations so that func(result)=value"""

    #get the amount of change we need to be below for the acc to be reached 1/10**acc
    accDelta = 10**(-acc)
    #calculate x from init_x
    x = init_x(val) if isinstance(init_x, functionType) else val if init_x is None else init_x
    # generate functons to calulate on hopfuly self explantory
    fun   = lambda x: eval(func) - val if isinstance(func,   str) else lambda x: func(x) - val
    dfun  = lambda x: eval(dfunc)      if isinstance(dfunc,  str) else dfunc
    ddfun = lambda x: eval(ddfunc)     if isinstance(ddfunc, str) else ddfunc
    # crate lambda to calculate the new x from old x using
    getDelta = lambda x: (2*fun(x)*dfun(x))/(2*dfun(x)**2-fun(x)*ddfun(x))
    
    # for i in range(maxIter) but this has mamory problems as 1 mil is a little large
    iterCounter = 0
    while iterCounter < maxIter:
        iterCounter += 1
        # calculate dx using lambda defined above
        delta = getDelta(x)
        # calculate x by substacting delta
        x -= delta
        # if acc reached retun value
        if delta < accDelta:
            return x
    # if iter lim reached check if warning should be raised
    if warn:
        warnings.warn(jpe.errors.jpeCalculationAbortedWarning("iter limit reached last delta is{delta}"))
    return x

def brent(fun, a=-inf, b=+inf, val=0, x0=None, rtol=_eps, atol=_eps, maxiter=500, mode=1): # original code from https://github.com/limix/brent-search/blob/master/brent_search/_brent.py
    """Seeks a minimum of a function via Brent's method.

    Given a function ``f`` with a minimum in the interval ``a <= b``, seeks a local
    minimum using a combination of golden section search and successive parabolic
    interpolation.
    Let ``tol = rtol * abs(x0) + atol``, where ``x0`` is the best guess found so far.
    It converges if evaluating a next guess would imply evaluating ``f`` at a point that
    is closer than ``tol`` to a previously evaluated one or if the number of iterations
    reaches maxiter.
    
    @param fun: Objective function to be minimized. or a string in witch case it will be turned into a function\n
    @type fun:  function

    @param a: Interval's lower limit. Defaults to ``-inf`` if it is a function:
                a is redefined as the output of the function with parameters val
    @type a:  float or function optional

    @param b: Interval's upper limit. Defaults to ``+inf``.
                if it is a function:
                b is redefined as the output of the function with parameters val
    @type b:    float or function optional

    @param val:Initial guess. Defaults to ``None``, which implies that::
                x0 = a + 0.382 * (b - a)
                f0 = f(x0)
                if function x0 will be the result of that function with input (val)
    @type val: float, function optional

    @param rtol: Relative tolerance. Defaults to ``1.4902e-08``.
    @type float: float

    @param atol: Absolute tolerance. Defaults to ``1.4902e-08``.
    @type atol: float

    @param maxiter: Maximum number of iterations.
    @type maxiter: int

    @returns:   float
                Best guess for x of the minimum, maximum,equalval to val of f,
                float
                value of generated function at position x, 
                int
                iteration number
    """

    # note this function war copyed char for char from https://github.com/limix/brent-search/blob/master/brent_search/_brent.py
    # so credit where it due howerver ive modified it afterwards
    
    # a, b: interval within the minimum should lie
    #       no function evaluation will be requested
    #       outside that range.
    # x0: least function value found so far (or the most recent one in
    #                                            case of a tie)
    # x1: second least function value
    # x2: previous value of x1
    # (x0, x1, x2): Memory triple, updated at the end of each interation.
    # u : point at which the function was evaluated most recently.
    # m : midpoint between the current interval (a, b).
    # d : step size and direction.
    # e : memorizes the step size (and direction) taken two iterations ago
    #      and it is used to (definitively) fall-back to golden-section steps
    #      when its value is too small (indicating that the polynomial fitting
    #      is not helping to speedup the convergence.)
    #
    #
    # References: Numerical Recipes: The Art of Scientific Computing
    # http://people.sc.fsu.edu/~jburkardt/c_src/brent/brent.c

    #build function so that the 0 positions of f are the val positions of fun
    # mode is 1 means we are looking for a minimum
    if mode == modes.minimum: f = lambda x: fun(x)  if isinstance(fun, functionType) else  eval(fun)
    # mode is 2 means we are looking for a maximum
    if mode == modes.maximum: f = lambda x: -fun(x) if isinstance(fun, functionType) else -eval(fun)
    # mode is 3 means we are looking fore a specific value
    if mode == modes.equalVal: f = lambda x: abs(fun(x) - val) if isinstance(fun, functionType) else abs(eval(fun) - val)

    if isinstance(b, functionType):
        b = b(val)
    
    if isinstance(a, functionType):
        a = a(val)

    if a > b:
        raise ValueError("'a' must be equal or smaller than 'b'")

    if x0 is None:
        x0 = a + _golden * (b - a)
        f0 = f(x0)
        
    if isinstance(x0, functionType):
        x0 = x0(val)
    else:
        if not (a <= x0 <= b):
            raise RuntimeError("'x0' didn't fall in-between 'a' and 'b', can be cecause of rounding error")

    x1 = x0
    x2 = x1
    niters = -1
    d = 0.0
    e = 0.0
    f1 = f0
    f2 = f1

    for niters in range(maxiter):

        m = 0.5 * (a + b)
        tol = rtol * abs(x0) + atol
        tol2 = 2.0 * tol

        # Check the stopping criterion.
        if abs(x0 - m) <= tol2 - 0.5 * (b - a):
            break

        r = 0.0
        q = r
        p = q

        # "To be acceptable, the parabolic step must (i) fall within the
        # bounding interval (a, b), and (ii) imply a movement from the best
        # current value x0 that is less than half the movement of the step
        # before last."
        #   - Numerical Recipes 3rd Edition: The Art of Scientific Computing.

        if tol < abs(e):
            # Compute the polynomial of the least degree (Lagrange polynomial)
            # that goes through (x0, f0), (x1, f1), (x2, f2).
            r = (x0 - x1) * (f0 - f2)
            q = (x0 - x2) * (f0 - f1)
            p = (x0 - x2) * q - (x0 - x1) * r
            q = 2.0 * (q - r)
            if 0.0 < q:
                p = -p
            q = abs(q)
            r = e
            e = d

        if abs(p) < abs(0.5 * q * r) and q * (a - x0) < p and p < q * (b - x0):
            # Take the polynomial interpolation step.
            d = p / q
            u = x0 + d

            # Function must not be evaluated too close to a or b.
            if (u - a) < tol2 or (b - u) < tol2:
                if x0 < m:
                    d = tol
                else:
                    d = -tol
        else:
            # Take the golden-section step.
            if x0 < m:
                e = b - x0
            else:
                e = a - x0
            d = _golden * e

        # Function must not be evaluated too close to x0.
        if tol <= abs(d):
            u = x0 + d
        elif 0.0 < d:
            u = x0 + tol
        else:
            u = x0 - tol

        # Notice that we have u \in [a+tol, x0-tol] or
        #                     u \in [x0+tol, b-tol],
        # (if one ignores rounding errors.)
        fu = f(u)

        # Housekeeping.

        # Is the most recently evaluated point better (or equal) than the
        # best so far?
        if fu <= f0:

            # Decrease interval size.
            if u < x0:
                if b != x0:
                    b = x0
            else:
                if a != x0:
                    a = x0

            # Shift: drop the previous third best point out and
            # include the newest point (found to be the best so far).
            x2 = x1
            f2 = f1
            x1 = x0
            f1 = f0
            x0 = u
            f0 = fu

        else:
            # Decrease interval size.
            if u < x0:
                if a != u:
                    a = u
            else:
                if b != u:
                    b = u

            # Is the most recently evaluated point at better (or equal)
            # than the second best one?
            if fu <= f1 or x1 == x0:
                # Insert u between (rank-wise) x0 and x1 in the triple
                # (x0, x1, x2).
                x2 = x1
                f2 = f1
                x1 = u
                f1 = fu
            elif fu <= f2 or x2 == x0 or x2 == x1:
                # Insert u in the last position of the triple (x0, x1, x2).
                x2 = u
                f2 = fu

    return x0, f0, niters + 1


def general(func, val, c, x=0, acc=10, maxIter=1_000, warn=False):
    """
    implementation of a genral aprocimation algorythem for fun, fun(result) = val, and c is the constant used

    given a function func we can find a solution for func(result) = value where result is the result of these calculations
    we can do this by substacting a multiple of func(x) from x

    @type func:   function, string
    @param func:        function we check against
            if string function is generated as lambda x: eval(func)

    @type val:    float
    @param val:        the value of the function at the end aka the value we want to get from func(result)

    @type c:      float
    @param c:        the number we multiply func(x) with for the approximation calculations

    @type acc:    int
    @param acc:        ammount of post comma digits to calculate for

    @type maxIter: int
    @param maxIter:        maximum amount of iterations before abort

    @type warn:   bool
    @param warn:        if true a warning is raised when max iter is reached


    @return: float
            the result ot the calculations so that func(result)=val 
    """
    # generate fun from func to simplyfy calulations
    fun = lambda x: func(x) - val if isinstance(func, functionType) else eval(func) - val
    #calculate acc delta same as all the others 1/10**acc
    accDelta = 10**(-acc)
    #commence algorythem
    # for i in range(maxIter) but this has mamory problems as 1 mil is a little large
    iterCounter = 0
    while iterCounter < maxIter:
        iterCounter += 1
        #calculate cahange from fun and c
        delta = fun(x)
        # update x
        x -= delta
        #if accuracy reached end search
        if abs(delta) < accDelta:
            return round(x, acc)
    # if warn ist tu complain about ending du to iter lim reach
    if warn:
        warnings.warn(jpe.errors.jpeCalculationAbortedWarning("iter limit reached last delta is{delta}"))
    return round(x, acc)