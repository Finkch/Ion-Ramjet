# This file defines what is included on a spacecraft.
#   Core/spacecraft
#   Scoop
#   Ionizer
#   Thruster
#   Tank
#   Reactor
# All these components have some mass
# Everything is in terms of SI units

import vector as v
import visuals as vis
from util import *


class Actor(object):
    def __init__(self, name, mass, radius):

        self.spacetime = v.spacetime()

        self.mass = mass

        self.shape = vis.shape(radius)

        # The most crucial part: the name
        self.name = name

    # Updates the craft
    def __call__(self, time_step):
        self.spacetime(time_step)

    def __str__(self):
        return self.name + "\n" + str(self.spacetime)
    
    def get_printout(self):
        return [
            f'{self.name}',
            f'{self.mass}',
            f'{self.pos()}'
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


# This is the core, the glue that holds everything together
class Spacecraft(Actor):
    def __init__(self, name, radius, core_mass, thruster, ionizer, scoop, tank, reactor):

        self.orientation = orientation()

        # Creates the craft from the components
        self.core_mass = core_mass
        self.thruster = thruster
        self.ionizer = ionizer
        self.scoop = scoop
        self.tank = tank
        self.reactor = reactor

        # Gets the mass of the craft
        super().__init__(name, self.get_mass(), radius)

    def __call__(self, time_step, fire):

        if fire:
            thrust = self.thruster(self.ionizer, self.reactor)
            force = radial_to_cartesian(thrust, self.orientation.theta, self.orientation.phi)
            self.force(force)

        super().__call__(time_step)

    
    # Returns the current mass of the craft
    def get_mass(self):
        mass = 0
        mass += self.core_mass
        mass += self.thruster.get_mass()
        mass += self.ionizer.get_mass()
        mass += self.scoop.get_mass()
        mass += self.tank.get_mass()
        mass += self.reactor.get_mass()

        return mass
    
    def get_printout(self):
        return [
            self.name,
            f'phi {self.orientation.phi:.2f}',
            f'{self.mass:.2e} kg',
            f'pos {hypo(self.pos()):.2e} m',
            f'vel {hypo(self.vel()):.2e} m/s'
        ]


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


# What produces the thrust
#   Accepts ionized gas and power
#   Outputs force
class thruster:
    def __init__(self, mass, v_e, max_F, max_P):

        self.mass = mass
        
        self.v_e = v_e              # Exhaust velocity
        self.max_F = max_F      # Max mass flow
        self.max_P = max_P

    def __call__(self, ionizer, reactor):
        return self.max_F
    
    def get_mass(self):
        return self.mass

# Ionizes inputted gas
#   Accepts deionized gas and power
#   Outputs ionized gas
class ionizer:
    def __init__(self, mass, power_per, in_flow, out_flow):
        
        self.mass = mass
        self.power_per = power_per
        self.in_flow = in_flow
        self.out_flow = out_flow

    
    def get_mass(self):
        return self.mass

# Scoops up gas from the interstellar medium
#   Accepts power
#   Outputs (mostly) deionized gas
class scoop:
    def __init__(self, mass, power, radius):
        
        self.mass = mass

        self.power = power
        self.radius = radius
    
    def get_mass(self):
        return self.mass

# Hold fuel
#   (Optionally) accepts gas
#   Outputs gas
class tank:
    def __init__(self, mass, max_fuel_mass, fuel):
        
        self.mass = mass

        self.max_fuel = max_fuel_mass
        self.fuel = fuel

    def get_mass(self):
        return self.mass + self.fuel

# Creates power
#   (Depends on type) accepts sun or fuel
#   Outputs power
class reactor:
    def __init__(self, mass, generation):
        
        self.mass = mass

        self.generation = generation
    
    def get_mass(self):
        return self.mass
