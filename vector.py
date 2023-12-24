# Defines basic vectors and their operations

import numpy as np

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
    
    def __neg__(self):
        return Vector(
            -self.x,
            -self.y,
            -self.z
        )
    
    # Overloads bitwise-and for cross product
    #   (a2*b3-a3*b2, a3*b1-a1*b3, a1*b2-a2*b1); thanks stack overflow
    #   Oh, of course, that's just the determinent - silly me    
    def __and__(self, other):
        return Vector(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    # Overloads bitwise-xor for dot product
    def __xor__(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z


    # Other class functions
    def __str__(self):
        return "\n\tx:\t{x:.2e}\n\ty:\t{y:.2e}\n\tz:\t{z:.2e}".format(x = self.x, y = self.y, z = self.z)
    
    
    # Returns the hypotenuse of the vector
    def hypo(self):
        return np.sqrt(sum([component ** 2 for component in self()]))
    
    # Returns the theta component of the radial vector
    def theta(self):

        # theta = arccos(z / r)
        return np.arccos(self.z / self.hypo())

    # Returns the phi component of the radial vector
    def phi(self):

        # phi = sgn(y) * arccos(x / rho)
        return np.sign(self.y) * np.arccos(self.x / Vector(self.x, self.y, 0).hypo())
    
    # Gets the orientation of this vector
    def orientation(self):
        return Orientation(self.theta(), self.phi())

    # Returns a vector normal to this one
    def normal(self):
        return self / self.hypo()
        
    

    # Returns one of the planes of the vector
    def plane(self, exclude = "z"):
        if exclude == "z":
            return (self.x, self.y)
        elif exclude == "y":
            return (self.x, self.y)
        else:
            return (self.y, self.z)
        



# Describes the orientation in space
class Orientation:
    def __init__(self, theta = 0, phi = 0):

        # Default orientation is based on the starting position
        self.theta = theta
        self.phi = phi

    # Calling orientation returns an array
    def __call__(self):
        return [self.theta, self.phi]


    # Orientation operations
    def __add__(self, other):

        if type(other) == "list":
            return Orientation(
                self.theta  + other[0],
                self.phi + other[1] 
            )
        else:
            return Orientation(
                self.theta + other.theta, 
                self.phi + other.phi
            )
    
    def __sub__(self, other):
        return Orientation(
            self.theta - other.theta,
            self.phi - other.phi
        )
    
    def __mul__(self, other):  # Multiplication by a constant
        return Orientation(
            self.theta * other,
            self.phi * other
        )

    def __rmul__(self, other):
        return Orientation(
            other * self.theta,
            other * self.phi
        )
    
    def __truediv__(self, other):   # Division by a constant
        return Orientation(
            self.theta / other,
            self.phi / other
        )
    
    def __rtruediv__(self, other):   # Division by a constant
        return Orientation(
            other / self.theta,
            other / self.phi
        )
    
    def __pow__(self, other):
        return Orientation(
            self.theta ** other,
            self.phi ** other
        )
    
    def __neg__(self):
        return Orientation(
            -self.theta,
            -self.phi
        )
    

    # String representation of Orientation
    def __str__(self):
        return f'\n\ttheta:\t{self.theta}\n\tphi:\t{self.phi}'
    
    # Orients in the direction of the specified vector
    def goto(self, vec):
        self.theta = vec.theta()
        self.phi = vec.phi()

    # Ensures the angle remains bounded
    def bound(self):
        self.theta = (self.theta + np.pi / 2) % np.pi - np.pi / 2
        self.phi = (self.phi + np.pi) % (2 * np.pi) - np.pi



    
# Holds position, velocity, and acceleration
class Spacetime:
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
        out += "Position:\t{mag:.2e}".format(mag = self.position.hypo()) + str(self.position)
        out += "\nVelocity:\t{mag:.2e}".format(mag = self.velocity.hypo()) + str(self.velocity)
        out += "\nAcceleration:\t{mag:.2e}".format(mag = self.acceleration_preview.hypo()) + str(self.acceleration_preview)

        return out


# Spacetime but includes angles
class AngularSpacetime(Spacetime):
    def __init__(self):
        super().__init__()

        self.angular_position = Orientation(np.pi / 2, 0)
        self.angular_velocity = Orientation()
        self.angular_acceleration = Orientation()
        self.angular_acceleration_preview = Orientation()
    
    # Updates angular spacetime
    def __call__(self, time_step = DEFAULT_TIME):
        super().__call__(time_step)

        # Updates position in space
        self.angular_velocity += self.angular_acceleration * time_step
        self.angular_position += self.angular_velocity * time_step

        # Captures a preview of the acceleration
        self.angular_acceleration_preview = self.acceleration

        # Bounds angular position.
        # The other dimensions should NOT be bounded
        self.angular_position.bound()

        # Resets acceleration
        self.angular_acceleration = Orientation()




# Splits a radial vector into its cartesian components.
# It is assumed that vec is a vector with the same orientation
# but a different magnitude
def radial_to_cartesian(radial, theta, phi):
    return Vector(
        radial * np.sin(theta) * np.cos(phi),
        radial * np.sin(theta) * np.sin(phi),
        radial * np.cos(theta)
    )