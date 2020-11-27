import math
import jpe.math.Jmath as Jmath

class Jfloat():
    
    def __init__(self, val, N=None): ## input val as 123.456|678 | commences periode

        if N is None:
            self.n, self.x = self._getCo(val)
        else:
            self.n, self.x = self._simplify((N, val))

        ##float.__init__(self, self.x / self.n)


    def _getCo(self, val):
        return self._simplify(self._getCo_2(val))

    def _simplify(self, co):
        n, x = co
        gcd = math.gcd(x, n)
        if n < 0: x, n = -x, -n
        return (n//gcd, x//gcd)
        
    
    def _getCo_2(self, val):
        if isinstance(val, str):
            return self._getCoFromStr(val)
        if isinstance(val, int):
            return 1, val
        if isinstance(val, float):
            return self._getCoFromStr(str(val))
        raise ValueError ('invalid literal for Jfloat(): ' + str(val))

    def _getCoFromStr(self, val):
        if not '.' in val:
            return 1, int(val)
        
        if not '|' in val:
            return self._getCoFromStr_simple(val)
        return self._getCoFromStr_wPer(val)

    def _getCoFromStr_simple(self, val):
        dot_idx = val.index('.')

        n = int(10 ** (len(val) - dot_idx- 1))
        x = int(val.replace('.', ''))
        return n, x

    def _getCoFromStr_wPer(self, val):
        val_copy = val
        per_idx = val.index('|')
        
        val_copy = val_copy[:per_idx]
        N, X = self._getCoFromStr_simple(val_copy)
        
        val = val.replace('.', '').replace('|', '.')
        N2, X2 = self._getCoFromStr_simple(val)
        
        x = X2 - X
        n = N2 * N - N
        return n, x

    def _getval(self):
        return self.x / self.n


    def __cmp__(self, other):  ## comparison
        other = _convertToJfloat(other)
        if self.x == other.x and self.n == other.n:
            return int(0)

        self_x, other_x, lcm = self._prep4op1(other)

        if self.x > other.x:
            return 1
        return -1

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __ne__(self, other):
        return self.__cmp__(other) != 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0
            
##    def __pos__(self)

    def __neg__(self): # negative object
        return Jfloat(-self.x, self.n)

    def __abs__(self): # abs value
        return Jfloat(abs(self.x), abs(self.n))

    def __invert__(self):
        return Jfloat(self.n, self.x)

##    def __invert__(self):

    def __round__(self, n): # rounds value
        return round(self._getval())

    def __floor__(self): ## return nearest in touwnwards
        return self.x // self.n

    def __ciel__(self):
        if self.x % self.n == 0:
            return self.__floor__()
        return self.__floot__() + 1

    def __trunc__(self):
        if self < 0:
            return __ciel__()
        return __floot__()
    
        

##__________________________________________________
    


    def _prep4op1(self, other):
        other = _convertToJfloat(other)
        
        lcm = Jmath.lcm(self.n, other.n)
        x = self.x
        X = other.x
        x = x * lcm // self.n
        X = X * lcm // other.n
        return x, X, lcm

    def _prep4op2(self, other):
        other = _convertToJfloat(other)
        
        x = self.x
        X = other.x
        n = self.n
        N = other.n
        return x, X, n, N

    def __add__(self, other):
        x, X, lcm = self._prep4op1(other)
        return Jfloat(X + x, lcm)
  

    def __sub__(self, other):
        x, X, lcm = self._prep4op1(other)
        return Jfloat(x - X, lcm)
        

    def __mul__(self, other):
        x, X, n, N = self._prep4op2(other)
        return Jfloat(x * X, n * N)

    def __floordiv__(self, other):
        num = self.__truediv__(other)
        return num.__floor__()

    def __truediv__(self, other):
        x, X, n, N = self._prep4op2(other)
        return Jfloat(x * N, X * n)

    # truediv

    def __mod__(self, other):
        return self - self.__floordiv__(other) * other

    def __exp__(self, other):
        x, X, n, N = self._prep4op2(other)
        if N != 1:
            raise ValueError
        return Jfloat(x ** X, n ** x)

## _________________________________________________________

    def __radd__(self, other):
        return self.__add__(other)

    def __rsub__(self, other):
        x, X, lcm = self._prep4op1(other)
        return Jfloat(X - x, lcm)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __rfloordiv__(self, other):
        num = self.__rtruediv__(other)
        return num.__floor__()

    def __rtruediv__(self, other):
        X, x, N, n = self._prep4op2(other)
        return Jfloat(x * N, X * n)

    def __rmod__(self, other):
        return other - self.__rmul__(self.__rfloordiv__(other))

    def __rexp__(self, other):
        X, x, N, n = self._prep4op2(other)
        if N != 1:
            raise ValueError
        return Jfloat(x ** X, n ** x)

## ________________________________________________________

    def __iadd__(self, other):
        return self.__add__(other)

    def __isub__(self, other):
        return self.__sub__(other)

    def __imul__(self, other):
        return self.__mul__(other)

    def __ifloordiv__(self, other):
        return self.__floordiv__(other)

    def __itruediv__(self, other):
        return self.__truediv__(other)

    def __imod__(self, other):
        return self.__mod__(other)

    def __iexp__(self, other):
        return self.__mod__(other)

## _____________________________________________________

    def __float__(self):
        return self.x / self.n

    def __int__(self):
        return int(self.__float__())

    def __Jfloat__(self):
        return self

## ______________________________________________________

    def __str__(self):
        return str(self.x) + ' / ' + str(self.n)

    def __unicode__(self):
        return self.__str__()

    def __format__(self, _):
        return self.__str__()

    def __repr__(self):
        return self.__str__()

    def __dir__(self):
        return self.x, self.n

    def __bool__(self):
        return self.x != 0

## _____________________________________________________

    def __getattr__(self, name):
        raise AttributeError (str(name))

## _____________________________________________________

    def __copy__(self):
        return Jfloat(self.x, self.n)

    def __deepcopy__(self):
        return self

## _____________________________________________________

    def __getstate__(self):
        return self.x, self.n

    def __setstate__(self, state):
        self.x, self.n = state


def _convertToJfloat(num):
    if isinstance(num, Jfloat):
        return num

    try:
        return num.__Jfloat__()
    except:
        return Jfloat(num)

