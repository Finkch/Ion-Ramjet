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
import orders as o
import numpy as np


class Actor(object):
    def __init__(self, name, mass, radius):

        self.spacetime = v.Spacetime()

        self.mass = mass

        self.shape = vis.Shape(radius)

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
    def __init__(self, name, radius, core_mass, thruster, ionizer, scoop, hydrogen_tank, ionized_tank, electric_tank, reactor):

        # Creates the craft from the components
        self.core_mass = core_mass
        self.thruster = thruster
        self.ionizer = ionizer
        self.scoop = scoop
        self.hydrogen_tank = hydrogen_tank
        self.ionized_tank = ionized_tank
        self.battery = electric_tank
        self.reactor = reactor

        self.thruster.spacecraft = self
        self.ionizer.spacecraft = self
        self.scoop.spacecraft = self
        self.tank.spacecraft = self
        self.reactor.spacecraft = self


        # Throttle ranges from 0 to 1
        self.throttle = o.Range(0, 0.01, 0, 1)

        self.force_preview = v.Vector()

        # Gets the mass of the craft
        super().__init__(name, self.get_mass(), radius)
        self.spacetime = v.AngularSpacetime()

    def __call__(self, time_step):

        self.reactor()

        if self.throttle.get() != 0:
            thrust = self.thruster(self.reactor, self.throttle, 100)
            force = v.radial_to_cartesian(-thrust, self.apos().theta, self.apos().phi)
            self.force(force)
            self.force_preview = force

        super().__call__(time_step)


    # Rotates the craft
    def rotate_cw(self):
        self.spacetime.angular_position.phi += 0.05

    def rotate_ccw(self):
        self.spacetime.angular_position.phi -= 0.05
    
    def goto_velocity(self):
        self.spacetime.angular_position.goto(self.vel())
    

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
    
    # Some getters
    def apos(self):
        return self.spacetime.angular_position
    
    def avel(self):
        return self.spacetime.angular_velocity
    
    def aacc(self):
        return self.spacetime.angular_acceleration
    
    # Returns a string for a printout
    def get_printout(self):
        return [
            self.name,
            f'phi {self.apos().phi:.2f}',
            f'mas {self.mass:.2e} kg',
            f'pos {self.pos().hypo():.2e} m',
            f'vel {self.vel().hypo():.2e} m/s',
            f'thr {self.force_preview.hypo():.2e} N'
        ]


# What produces the thrust
#   Accepts ionized gas and power
#   Outputs force
class thruster:
    def __init__(self, mass, v_e, max_F, max_P):

        self.spacecraft = None

        self.mass = mass
        
        self.v_e = v_e          # Exhaust velocity
        self.max_F = max_F      # Max mass flow
        self.max_P = max_P

        self.m_dot = self.max_F / self.v_e

    def __call__(self, reactor, throttle, fuel):

        throughput = min(fuel / self.m_dot, throttle.get(), reactor.percent)

        reactor.request(self.max_P * throughput)

        return self.max_F * throughput
    
    def get_mass(self):
        return self.mass

# Ionizes inputted gas
#   Accepts deionized gas and power
#   Outputs ionized gas
class ionizer:
    def __init__(self, mass, power_per, in_flow, out_flow):
        
        self.spacecraft = None

        self.mass = mass
        self.power_per = power_per
        self.in_flow = in_flow
        self.out_flow = out_flow

    def __call__(self, reactor, flow_in):
        
        to_ionize = flow_in * self.power_per
        reactor.request(to_ionize)

        return to_ionize * reactor.percent

        # Requests power
        #reactor.requested_power(self.power)

    def get_mass(self):
        return self.mass

# Scoops up gas from the interstellar medium
#   Accepts power
#   Outputs (mostly) deionized gas
class scoop:
    def __init__(self, mass, power, radius):
        
        self.spacecraft = None

        self.mass = mass

        self.power = power
        self.radius = radius

    def __call__(self, reactor, spacetime, density, time_step):

        # Requests power
        reactor.request(self.power)

        # How well alligned the craft is to the ISM
        #   Alternatively, we could compare the angles returned by pos and vel
        sweep = spacetime.position.normal() ^ spacetime.velocity.normal()

        # If the sweep is negative, then it means the craft is facing backwards
        sweep = max(0, sweep)

        current_radius = np.pi * (self.radius * reactor.percent) ** 2

        effective_area = sweep * current_radius

        # This is volume per second!
        swept_volume = effective_area * spacetime.velocity.hypo()

        # Returns the rate of collected Hydrogen
        return swept_volume * density
    
    def get_mass(self):
        return self.mass

# Hold fuel
#   (Optionally) accepts gas
#   Outputs gas
class tank:
    def __init__(self, mass, max_fuel_mass, fuel):
        
        self.spacecraft = None

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
        
        self.spacecraft = None

        self.mass = mass

        self.generation = generation

        # Requested power allows the reactor to allocate thrust next sim
        self.requested_power = 0

        # What percent of requested power this can supply
        self.percent = 0
    
    def __call__(self):
        
        # Calculates the percent of requested power this can generate
        #   Upper limit of 1
        self.percent = 1 if self.generation > self.requested_power else self.generation / self.requested_power

        # Resets requested power
        self.requested_power = 0
    
    # Requests power for next step
    def request(self, amount):
        self.requested_power += amount

    
    def get_mass(self):
        return self.mass


# All ship parts have some mass
class Part:
    def __init__(self, name, mass):
        self.mass = mass
    
    def get_mass(self):
        return self.mass

# Produces something
class Generator(Part):
    def __init__(self, name, mass, production_rate, tank = None, consumptions = None):
        super().__init__(name, mass)

        # How quickly it can produce
        self.production = production_rate
        
        # Consumption rates and inputs stored in a dictionary:
        #   conumsptions = {
        #       '$fuel_name': {
        #           'fuel': $rate_consumed
        #           'tank': $regulator
        #       }
        #   }
        self.consumptions = consumptions

        # Where to output to
        self.tank = tank

        # The owner of this part
        self.spacecraft = None

    # Requests the items to be consumed
    def request(self):
        # Asks each part for fuel
        for key in self.consumptions.keys():
            self.consumptions[key]['tank'].request(self, self.consumptions[key]['fuel'])

    # Produces
    def produce(self):

        # Gets what percent this generator may produce
        throttle = 1
        for key in self.consumptions.keys():
            throttle = min(throttle, self.consumptions[key]['tank'].output(self))

        # Refunds regulators for fuel this was unable to use
        if throttle < 1:
            for key in self.consumptions.keys():
                self.consumptions[key]['tank'].input(self, self.consumptions[key]['fuel'] * (self.consumptions[key]['tank'].output(self) - throttle))

        # Calculates how much this generator produces        
        output = self.production * throttle


        # Places the output in the correct spot

        if not self.output:
            return output

        self.tank().input(output)

        

# Holds stuff and checks the rate
class Regulator(Part):
    def __init__(self, name, mass, capacity, fuel_mass = 0):
        super().__init__(name, mass)

        # The size of the tank
        self.max_capacity = capacity
        self.capacity = 0

        # Mass of the fuel per unit of capacity
        self.density = fuel_mass

        # The requested flow rates
        self.outputs = []
        self.requests = []
        self.requested = 0


        # The owner of this part
        self.spacecraft = None

    # Handles one step of simulation
    def __call__(self, time_step):
        self.requests = {}
        self.outputs = {}
        self.requested = 0

    # Adds a request
    def add_request(self, source, amount, priority):
        self.request.append({'fuel': amount, 'source': source})
        self.requested += amount

    # Pipes fuel into the tank
    def input(self, fuel, source = None):
        
        # Adds fuel to the tank
        self.capacity + fuel

        # Caps the amount of fuel
        if self.capacity > self.max_capacity:
            overflow = self.capacity - self.max_capacity # Overflow is currently ditched overboard
            self.capacity = self.max_capacity
        
    # Sorts requests by priority; highest priority first
    def sort_requests(self):
        self.requests.sort(key = lambda x: (x['fuel']))


    # Overload get mass to return the mass of this part plus its fuel
    def get_mass(self):
        return super().get_mass() + self.capacity * self.density