import math

def is_prime(n):
    if n == 1:
        return False
    
    if n in [2, 3]:
        return True
    
    if n % 2 == 0:
        return False
    
    divisor = int(math.sqrt(n))
    while divisor > 2:
        if n % divisor == 0:
            return False
        divisor -= 1

    return True
        
        
assert(is_prime(5))
assert(is_prime(31))
assert(not is_prime(64))