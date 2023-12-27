# One 'thing' that is simulated
from finkchlib.vector import *

class Actor(object):
    def __init__(self, name, mass, radius):

        self.spacetime = Spacetime()

        self.mass = mass

        self.radius = radius
        self.colour = 'white'

        # The most crucial part: the name
        self.name = name

    # Updates the craft
    def __call__(self, time_step):
        self.spacetime(time_step)

    def __str__(self):
        return self.name + "\n" + str(self.spacetime)
    
    def get_printout(self):
        return [
            self.name,
            f'mas {self.mass:.2e} kg',
            f'pos {self.pos().hypo():.2e} m',
            f'vel {self.vel().hypo():.2e} m/s',
        ]
                
    
    # Exerts a force on the actor
    def force(self, force):
        # Imparts the force as acceleration on the craft
        self.spacetime.acceleration += force / self.mass

    # Some getters
    def pos(self, dir = -1):
        if dir == -1:
            return self.spacetime.position
        else:
            return self.spacetime.position()[dir]
    
    def vel(self, dir = -1):
        if dir == -1:
            return self.spacetime.velocity
        else:
            return self.spacetime.velocity()[dir]
        
    def acc(self, dir = -1):
        if dir == -1:
            return self.spacetime.acceleration
        else:
            return self.spacetime.acceleration()[dir]
