# Defines basic vectors and their operations
import util

# Default step in time, in seconds
DEFAULT_TIME = 10

class vector:
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
            return vector(
                self.x + other[0],
                self.y + other[1],
                self.z + other[2]
            )
        else:
            return vector(
                self.x + other.x, 
                self.y + other.y,
                self.z + other.z
            )
    
    def __sub__(self, other):
        return vector(
            self.x - other.x, 
            self.y - other.y,
            self.z - other.z
        )
    
    def __mul__(self, other):  # Multiplication by a constant
        return vector(
            self.x * other,
            self.y * other,
            self.z * other
        )

    def __rmul__(self, other):
        return vector(
            other * self.x,
            other * self.y,
            other * self.z
        )
    
    def __truediv__(self, other):   # Division by a constant
        return vector(
            self.x / other,
            self.y / other,
            self.z / other
        )
    
    def __rtruediv__(self, other):   # Division by a constant
        return vector(
            other / self.x,
            other / self.y,
            other / self.z
        )
    
    def __pow__(self, other):
        return vector(
            self.x ** other,
            self.y ** other,
            self.z ** other
        )

    # Other class functions
    def __str__(self):
        return "\n\tx:\t{x:.2e}\n\ty:\t{y:.2e}\n\tz:\t{z:.2e}".format(x = self.x, y = self.y, z = self.z)
    
    
    def invert(self):
        return vector(
            self.x * -1,
            self.y * -1,
            self.z * -1
        )

    # Returns the magnitude of the position
    def mag(self):
        return util.hypo(self())
    

    # Returns one of the planes of the vector
    def plane(self, exclude = "z"):
        if exclude == "z":
            return (self.x, self.y)
        elif exclude == "y":
            return (self.x, self.y)
        else:
            return (self.y, self.z)



    
# Holds position, velocity, and acceleration
class spacetime:
    def __init__(self):

        self.time = 0

        self.position = vector()
        self.velocity = vector()
        self.acceleration = vector()

        # Since acceleration necessarily resets, this
        # is use to view acceleration
        self.acceleration_preview = vector()
    
    # Calling spacetime updates it by one step
    def __call__(self, time_step = DEFAULT_TIME):
        
        self.time += time_step

        # Updates position in space
        self.velocity += self.acceleration * time_step
        self.position += self.velocity * time_step

        # Captures a preview of the acceleration
        self.acceleration_preview = self.acceleration

        # Resets acceleration
        self.acceleration = vector()

    def __str__(self):
        out = ""
        out += "Position:" + str(self.position)
        out += "\nVelocity:" + str(self.velocity)
        out += "\nAcceleration:" + str(self.acceleration_preview)

        return out
    