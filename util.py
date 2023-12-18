# Several helpful utility functions
import math

# Returns the hypotenuse of a vector
def hypo(vec):
    
    # Sums the squares of each component and returns their square root
    hypo = 0
    for component in vec:
        hypo += component ** 2
    return math.sqrt(hypo)
