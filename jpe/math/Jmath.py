import math

def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

def round_decimal(a, pres=1):
    pres = int(pres)
    return int(a / 10 ** pres) * 10 ** pres
