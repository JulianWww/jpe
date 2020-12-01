"mathematical utils mainly for jfloat"
import math

def lcm(a, b):
    """smalest common multiple
    
    compute smalerst common multiple of a and b
    @param a: the first number to calculate
    @type a: int,
    @param b: the second number to calculate
    @type b: int
    @return: an int being the largest common multibple of a and b"""
    return abs(a * b) // math.gcd(a, b)

def round_decimal(a, pres=1):
    """round function
    
    depricated"""
    pres = int(pres)
    return int(a / 10 ** pres) * 10 ** pres
