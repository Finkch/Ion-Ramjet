# Defines basic vectors and their operations
import util

class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    # Calling a vector will return its components
    def __call__(self):
        return [self.x, self.y, self.z]



    # Vector operations
    def __add__(self, other):
        return Vector(
            self.x + other.x, 
            self.y + other.y,
            self.z + other.z)
    
    def __sub__(self, other):
        return Vector(
            self.x - other.x, 
            self.y - other.y,
            self.z - other.z)
    

    
    # Returns the magnitude of the position
    def mag(self):
        return util.hypo(self())