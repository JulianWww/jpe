import numpy as np
import jpe.Jfloat
import math

def jVectorTypeErrorMessage(other, operation):
    raise TypeError(f"jpe.vector dosnt suport {operation} operation with values of type {type(other)} if u think this schould be the case plz write me a message under Julian.wandhoven@fgz.ch")

def dot(u, v):
    return u._arr.dot(v._arr)

def cross(u, v):
    return vector(np.cross(u._arr, v._arr))

def getAngle(u, v):
    return math.acos(dot(u, v) /(v.__abs__() * u.__abs__()))

def det(v):
    return np.linalg.det(v)

def resultingForce(*vectors):
    try:
        vec = vectors[0]
        for cvec in vectors[1:]:
            vec = vec + cvec
    except:
        raise ValueError("dimentions do not match")
    return vec
    


class vector():
    def __init__(self, *val):
        if isinstance(val[0], np.ndarray):
            self._arr = val[0]
        else: self._arr = np.array(val)
        if (len(self._arr.shape)) != 1:
            raise ValueError(f"cant convert {self._arr} to vector")
        
    def __str__(self):
        return f"vector ({self._arr.__str__()[1:-1]})"
# addition
    def __add__(self, other):
        if isinstance(other, vector):
            return vector(self._arr + other._arr)
        jVectorTypeErrorMessage(other, "addition")

    def __radd__(self, other): return self.__add__(other)


#subraction
    def __sub__(self, other):
        if isinstance(other, vector):
            return vector(self._arr - other._arr)
        jVectorTypeErrorMessage(other, "diverentiation")

    def __rsub__(self, other):
        if isinstance(other, vector):
            return vector(other._arr - self._arr)
        jVectorTypeErrorMessage(other, "diverentiation")

    
#scalar
        #mul
    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(jpe.Jfloat.Jfloat):
            return vector(self._arr * other)
        else:
            jVectorTypeErrorMessage(other, "scalar")

    def __rmul__(self, other): return self.__mul__(other)
    
    
    #div    
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(jpe.Jfloat.Jfloat):
            return vector(self._arr / other)
        else:
            jVectorTypeErrorMessage(other, "scalar")

    def __floordiv__(self, other):
        if isinstance(other, int) or isinstance(other, float) or isinstance(jpe.Jfloat.Jfloat):
            return vector(self._arr // other)
        else:
            jVectorTypeErrorMessage(other, "floor scalar")

#lengths
    def __abs__(self):
        return np.linalg.norm(self._arr)

    def unit(self):
        return vector(self._arr / self.__abs__())

#muls
    def dot(self, other):
        return dot(self, other)

    def cross(self, other):
        return cross(self, other)

    def getAngle(s, o):
        return getAngle(s, o)

    def det(self):
        return det(self)
    
    def __neg__(self):
        return vector(-self._arr)

    def __getitem__(self, idx):
        return self._arr[idx]

    def __repr__(self): return self.__str__()
        
