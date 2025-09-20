import math

def mcd(a, b):
    return math.gcd(a, b)

def mcm(a, b):
    return abs(a * b) // mcd(a, b)

print(mcd(12, 18)) 
print(mcm(12, 18))  
