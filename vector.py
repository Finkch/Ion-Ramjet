# Defines basic vectors and their operations
from util import *

# Default step in time, in seconds
DEFAULT_TIME = 10

class Vector:
    def __init__(self, x = 0, y = 0, z = 0):
        self.x = x
        self.y = y
        self.z = z
    
    # Calling a vector will return its components
    def __call__(self):
        return [self.x, self.y, self.z]



    # Vector operations
    def __add__(self, other):

        if type(other) == "list":
            return Vector(
                self.x + other[0],
                self.y + other[1],
                self.z + other[2]
            )
        else:
            return Vector(
                self.x + other.x, 
                self.y + other.y,
                self.z + other.z
            )
    
    def __sub__(self, other):
        return Vector(
            self.x - other.x, 
            self.y - other.y,
            self.z - other.z
        )
    
    def __mul__(self, other):  # Multiplication by a constant
        return Vector(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __rmul__(self, other):
        return Vector(
            other * self.x,
            other * self.y,
            other * self.z
        )
    
    def __truediv__(self, other):   # Division by a constant
        return Vector(
            self.x / other,
            self.y / other,
            self.z / other
        )
    
    def __rtruediv__(self, other):   # Division by a constant
        return Vector(
            other / self.x,
            other / self.y,
            other / self.z
        )
    
    def __pow__(self, other):
        return Vector(
            self.x ** other,
            self.y ** other,
            self.z ** other
        )

    # Other class functions
    def __str__(self):
        return "\n\tx:\t{x:.2e}\n\ty:\t{y:.2e}\n\tz:\t{z:.2e}".format(x = self.x, y = self.y, z = self.z)
    
    
    def invert(self):
        return Vector(
            self.x * -1,
            self.y * -1,
            self.z * -1
        )

    # Returns the magnitude of the position
    def mag(self):
        return hypo(self())
    
    # Calculates the dot-product between two vectors
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    # Caclulates the cross-product between two vectors
    #   (a2*b3-a3*b2, a3*b1-a1*b3, a1*b2-a2*b1); thanks stack overflow
    #   Oh, of course, that's just the determinent - silly me
    def cross(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
        
    

    # Returns one of the planes of the vector
    def plane(self, exclude = "z"):
        if exclude == "z":
            return (self.x, self.y)
        elif exclude == "y":
            return (self.x, self.y)
        else:
            return (self.y, self.z)
        


# Describes the orientation in space
class orientation:
    def __init__(self):

        # Default orientation is based on the starting position
        self.theta = 0
        self.phi = 0
    
    # Orients in the direction of the specified vector
    def goto(self, vec):
        self.theta = theta(vec)
        self.phi = phi(vec)



    
# Holds position, velocity, and acceleration
class spacetime:
    def __init__(self):

        self.time = 0

        self.position = Vector()
        self.velocity = Vector()
        self.acceleration = Vector()

        # Since acceleration necessarily resets, this
        # is use to view acceleration
        self.acceleration_preview = Vector()
    
    # Calling spacetime updates it by one step
    def __call__(self, time_step = DEFAULT_TIME):
        
        self.time += time_step

        # Updates position in space
        self.velocity += self.acceleration * time_step
        self.position += self.velocity * time_step

        # Captures a preview of the acceleration
        self.acceleration_preview = self.acceleration

        # Resets acceleration
        self.acceleration = Vector()

    def __str__(self):
        out = ""
        out += "Position:\t{mag:.2e}".format(mag = hypo(self.position)) + str(self.position)
        out += "\nVelocity:\t{mag:.2e}".format(mag = hypo(self.velocity)) + str(self.velocity)
        out += "\nAcceleration:\t{mag:.2e}".format(mag = hypo(self.acceleration_preview)) + str(self.acceleration_preview)

        return out