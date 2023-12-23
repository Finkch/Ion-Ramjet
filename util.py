# Several helpful utility functions
import numpy as np
import vector as v
import constants as c

# Returns the hypotenuse of a vector
def hypo(vec):

    # Sums the squares of each component and returns their square root
    hypo = 0
    for component in vec():
        hypo += component ** 2
    return np.sqrt(hypo)


# Returns the theta component of the radial vector
def theta(vec):

    # theta = arccos(z / r)
    return np.arccos(vec.z / hypo(vec))

# Returns the phi component of the radial vector
def phi(vec):

    # phi = sgn(y) * arccos(x / rho)
    return np.sign(vec.y) * np.arccos(vec.x / hypo(v.Vector(vec.x, vec.y)))


# Splits a radial vector into its cartesian components.
# It is assumed that vec is a vector with the same orientation
# but a different magnitude
def radial_to_cartesian(radial, theta, phi):
    return v.Vector(
        radial * np.sin(theta) * np.cos(phi),
        radial * np.sin(theta) * np.sin(phi),
        radial * np.cos(theta)
    )


# Calculates the diference between vectors
def dif(a, b):
    return hypo(a - b)




# Tracks orders of magnitude and changing between them
class Orders:
    def __init__(self, initial, step_size = 1, digits = 1, minimum = -50, maximum = 150):
        self.step_size = step_size
        self.digits = digits if digits < 9 else 9 # Enforces an upper limit on digits
        self.set_order(initial)
        self.minimum = minimum
        self.maximum = maximum

    # Given a number, extract the scale and the order
    def set_order(self, num):

        # Extracts the leading digits
        self.scale = float(f'{num:.8e}'[:1 if self.digits == 1 else self.digits + 1]) # Accounts for the peroid
        
        # Extracts the order of magnitude
        self.order = int(np.log10(num))

    # Returns the number the order represents
    def get_order(self):
        return self.scale * 10 ** self.order


    # Increases the simulatoin rate
    def increase(self, multiplier = 1):

        # Increases scale
        self.scale += self.step_size * multiplier

        # Hanlde boundry changes
        if self.scale >= 10:
            if self.increase_order():
                self.scale = 1
            else:
                self.scale -= self.step_size * multiplier
            
    
    # Significantly increases the goal
    def increase_order(self):

        # Prevents the order from going above the maximum
        if self.order >= self.maximum:
            self.order = self.maximum
            return False
        
        self.order += 1
        return True

    # Descreases the simulation rate
    def decrease(self, multiplier = 1):
        
        # Descreases scale
        self.scale -= self.step_size * multiplier

        # Handles boundry change
        if self.scale < 1:
            if self.decrease_order():
                self.scale = 10 - self.step_size
            else:
                self.scale = 1

    # Significantly decreases the goal
    def decrease_order(self):

        # Prevents going below the minimum
        if self.order <= self.minimum:
            self.order = self.minimum
            return False
        
        self.order -= 1
        return True

