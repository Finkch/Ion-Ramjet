# This file defines what is included on a spacecraft.
#   Core/spacecraft
#   Scoop
#   Ionizer
#   Thruster
#   Tank
#   Reactor
# All these components have some mass



# This is the core, the glue that holds everything together
class spacecraft:
    def __init__(self, core_mass, thruster, ionizer, scoop, tank, reactor):

        # Creates the craft from the components
        self.core_mass = core_mass
        self.thruster = thruster
        self.ionizer = ionizer
        self.scoop = scoop
        self.tank = tank
        self.reactor = reactor

        # Gets the mass of the craft
        self.total_mass = 0
        self.total_mass = self.get_mass()
    
    # Returns the current mass of the craft
    def get_mass(self):
        mass = 0
        mass += self.core_mass
        mass += self.thruster.mass
        mass += self.ionizer.mass
        mass += self.scoop.mass
        mass += self.tank.mass
        mass += self.reactor.mass

        return mass
    

# What produces the thrust
#   Accepts ionized gas and power
#   Outputs force
class thruster:
    def __init__(self, mass, v_e, thrust_per, power_per):

        self.mass = mass
        
        self.v_e = v_e    # Exhaust velocity
        self.thrust_per = thrust_per
        self.power_per = power_per

# Ionizes inputted gas
#   Accepts deionized gas and power
#   Outputs ionized gas
class ionizer:
    def __init__(self):
        pass

# Scoops up gas from the interstellar medium
#   Accepts power
#   Outputs (mostly) deionized gas
class scoop:
    def __init__(self):
        pass

# Hold fuel
#   (Optionally) accepts gas
#   Outputs gas
class tank:
    def __init__(self):
        pass

# Creates power
#   (Depends on type) accepts sun or fuel
#   Outputs power
class reactor:
    def __init__(self):
        pass