"a vector implementation"

import numpy as np
import jpe.Jfloat
import math

def jVectorTypeErrorMessage(other, operation):
    """raise invalid other variable operation error

    error type is TypeErorr with message jpe.math.linalg.vector dosnt suport {operation} operation with values of type {type(other)}...
    
    @param operation: witchoperation raised the error
    @type operation: string
    @param other: the other variable that the operation was performed with
    @type other: object aka any
    """
    raise TypeError(f"jpe.math.linalg.vector dosnt suport {operation} operation with values of type {type(other)} if u think this schould be the case plz write me a message under Julian.wandhoven@fgz.ch")

def dot(u, v):
    """vector dot product

    computes the vector dot product of u and v
    @param u: vector 1 of the dot product
    @type u: vector
    @param v: vector 2 of the dot product
    @type v: vector
    @return: a float being the dot product of the vectrors
    """
    return u._arr.dot(v._arr)

def cross(u, v):
    """vector cross product

    computes the vector cross product of u and v
    if invalid vector size raise a value error
    @param u: vector 1 of the cross product
    @type u: vector in 3 dimentions
    @param v: vector 2 of the cross product
    @type v: vector in 3 dimentions
    @return: a vector being the dot product of the vectrors
    """
    if u._arr.size != 3 or u._arr.size != 3:
        raise ValueError("invalid vector dimentions for cross product beween {u} and {v}")
    return vector(np.cross(u._arr, v._arr))

def getAngle(u, v):
    """compute the angle between 2 vectors

    @param u: one of the 2 vectors we want to calculat the angle between
    @type u: vector
    @param v: the other vector
    @type v: vector
    @return: a float being the angle calculated by math.acos
    """
    return math.acos(dot(u, v) /(v.__abs__() * u.__abs__()))

def det(v):
    """computes the deteminant of the vector

    @param v: the vector whoms deteminant we want to calculate
    @type v: vector
    @return: the determinant 
    """
    return np.linalg.det(v)

def resultingForce(*vectors):
    """calculates the resulting force crated by a set of vecors acting on the same point

    mainly for physiks calculations
    @param vectors: the vectors acting on the point
    @type vectors: *vectors so a collection of vectors
    """
    try:
        vec = vectors[0]
        for cvec in vectors[1:]:
            vec = vec + cvec
    except:
        raise ValueError("dimentions do not match")
    return vec
    

"vector"
class vector():
    """a vector data type"""
    def __init__(self, *val):
        """initiate vector with values *val

        crates a vector with arears *val
        @param *val: values of the vector
        @type *val: a collection of floats or ints
        """
        if isinstance(val[0], np.ndarray):
            self._arr = val[0]
        else: self._arr = np.array(val)
        if (len(self._arr.shape)) != 1:
            raise ValueError(f"cant convert {self._arr} to vector")
        
    def __str__(self):
        "converts vector to string"
        return f"vector ({self._arr.__str__()[1:-1]})"
# addition
    def __add__(self, other):
        """+ operation
        
        add 2 vectors togather using the + operation"""
        if isinstance(other, vector):
            return vector(self._arr + other._arr)
        jVectorTypeErrorMessage(other, "addition")

    def __radd__(self, other): 
        """+ operation

        see __add__
        """
        return self.__add__(other)


#subraction
    def __sub__(self, other):
        """- substract a vector from another

        substract other vector from self vector
        """
        if isinstance(other, vector):
            return vector(self._arr - other._arr)
        jVectorTypeErrorMessage(other, "diverentiation")

    def __rsub__(self, other):
        """- substract a vector from another

        substract self vector from other vector
        """
        if isinstance(other, vector):
            return vector(other._arr - self._arr)
        jVectorTypeErrorMessage(other, "diverentiation")

    
#scalar
        #mul
    def __mul__(self, other):
        """* operationo
        multiplies a vector by a 1 dim scalar
        @param other: the scalar that the vector is multiplied with
        @type other: float or int or somthing that can be converted to a float
        @return: the scaled vector
        """
        if isinstance(other, int) or isinstance(other, float):# or isinstance(jpe.Jfloat.Jfloat):
            return vector(self._arr * other)
        else:
            try:
                self.__mul__(float(other))
            except:
                jVectorTypeErrorMessage(other, "scalar")

    def __rmul__(self, other): 
        """* operationo
        multiplies a vector by a 1 dim scalar
        @param other: the scalar that the vector is multiplied with
        @type other: float or int or somthing that can be converted to a float
        @return: the scaled vector
        """
        return self.__mul__(other)
    
    
    #div    
    def __truediv__(self, other):
        """/ operationo
        divides a vector by a 1 dim scalar
        @param other: the scalar that the vector is multiplied with
        @type other: float or int or somthing that can be converted to a float
        @return: the scaled vector
        """
        if isinstance(other, int) or isinstance(other, float) or isinstance(jpe.Jfloat.Jfloat):
            return vector(self._arr / other)
        else:
            jVectorTypeErrorMessage(other, "scalar")

    def __floordiv__(self, other):
        """// operationo
        divides a vector by a 1 dim scalar using floor division
        @param other: the scalar that the vector is multiplied with
        @type other: float or int or somthing that can be converted to a float
        @return: the scaled vector
        """
        if isinstance(other, int) or isinstance(other, float) or isinstance(jpe.Jfloat.Jfloat):
            return vector(self._arr // other)
        else:
            jVectorTypeErrorMessage(other, "floor scalar")

#lengths
    def __abs__(self):
        """|vec|

        @return: a float being the lenth of the vector using the pythegoream therum
        """
        return np.linalg.norm(self._arr)

    def unit(self):
        """computes the unit vector

        @return: unitvector of the vector the function is performed on
        """
        return vector(self._arr / self.__abs__())

#muls
    def dot(self, other):
        """vector dot product

        computes the vector dot product of u and v
        except that self is v
        @param u: vector 1 of the dot product
        @type u: vector
        @param v: vector 2 of the dot product
        @type v: vector
        @return: a float being the dot product of the vectrors
        """
        return dot(self, other)

    def cross(self, other):
        """vector cross product

        computes the vector crossproduct of u and v
        except that self is v
        @param u: vector 1 of the cross product
        @type u: vector
        @param v: vector 2 of the cross product
        @type v: vector
        @return: a float being the cross product of the vectrors
        """
        return cross(self, other)

    def getAngle(s, o):
        """compute the angle between 2 vectors
        u and v, v being self

        @param u: one of the 2 vectors we want to calculat the angle between
        @type u: vector
        @param v: the other vector
        @type v: vector
        @return: a float being the angle calculated by math.acos
        """
        return getAngle(s, o)

    def det(self):
        """computes the deteminant of the vector

        @return: the determinant"""
        return det(self)
    
    def __neg__(self):
        "get the vector facing the other direction"
        return vector(-self._arr)

    def __getitem__(self, idx):
        """[]
        returns the value of the vector on domention indx
        @param idx: witch dimentions u want to get
        @type idx: int or slice
        @return: vectors value on dimention idx"""
        return self._arr[idx]
    
    def __setitem__(self, idx, val):
        """[]=
        sets the vecor at idx to val
        @param idx: index at witch to set
        @type idx: int
        @param val: the value the vector[idx] schould have
        @type val: float or int"""
        self._arr[idx] = val

    def __repr__(self):
        "see str conversrion methode"
        return self.__str__()
        
