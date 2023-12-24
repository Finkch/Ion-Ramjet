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
    #def __init__(self, name, radius, core_mass, thruster, ionizer, scoop, hydrogen_tank, ionized_tank, electric_tank, reactor):
    def __init__(self, name, radius, core_mass, generators, regulators, thruster):

        # Creates the craft from the components
        self.core_mass = core_mass

        self.generators = generators
        self.regulators = regulators

        # The thruster is just another generator, but we need to grab its output
        self.thruster = thruster


        # Throttle ranges from 0 to 1
        self.throttle = o.Range(0, 0.01, 0, 1)

        self.force_preview = v.Vector()

        # Gets the mass of the craft
        super().__init__(name, self.get_mass(), radius)
        self.spacetime = v.AngularSpacetime()

        self.mass = self.get_mass()

    def __call__(self, time_step):

        self.thruster.request(self.throttle.get())
        for part in self.generators.values():
            part.request()

        for part in self.regulators.values():
            part.process()

        for part in self.generators.values():
            part.produce()
        
        thrust = self.thruster.produce()

        for part in self.regulators.values():
            if isinstance(part, Tank):
                part.reset(time_step)
            else:
                part.reset()

        
        # Converts the generated thrust into a vector
        #thrust = self.thruster(self.ionizer, self.reactor, self.throttle)
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
        mass = self.core_mass
        
        for part in self.generators.values():
            mass += part.get_mass()
        
        for part in self.regulators.values():
            mass += part.get_mass()

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

    def get_printout_regulators(self):
        return [str(part) for part in self.regulators.values()]




# All ship parts have some mass
class Part:
    def __init__(self, name, mass):
        self.name = name
        self.mass = mass
    
    def get_mass(self):
        return self.mass

# Produces something
class Generator(Part):
    def __init__(self, name, mass, production_rate, tank = None, consumptions = {}):
        super().__init__(name, mass)

        # How quickly it can produce
        self.production = production_rate

        # How quickly it is currently producing
        self.rate = 0
        
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
    def request(self, throttle = 1):
        self.rate = self.production * throttle

        # Asks each part for fuel
        for key in self.consumptions.keys():
            self.consumptions[key]['tank'].add_request(self, self.consumptions[key]['fuel'] * throttle)

    # Produces
    def produce(self):

        # Gets what percent this generator may produce
        throttle = 1
        for key in self.consumptions.keys():
            throttle = min(throttle, self.consumptions[key]['tank'].output(self)['percent'])

        # Refunds regulators for fuel this was unable to use
        #if throttle < 1:
        for key in self.consumptions.keys():
            output = self.consumptions[key]['tank'].output(self)

            percent = 1 - throttle / output['percent'] if output['percent'] != 0 else 0
            refunded = output['fuel'] * percent

            self.consumptions[key]['tank'].input(refunded, self)

        # Calculates how much this generator produces        
        produced = self.rate * throttle


        # Places the output in the correct spot

        if not self.tank:
            return produced

        self.tank.input(produced)

        

# Holds stuff and checks the rate
class Regulator(Part):
    def __init__(self, name, mass, capacity, fuel_density = 1, unit = 'kg/s'):
        super().__init__(name, mass)

        # How much fuel is flowing into the tank
        self.capacity = capacity
        self.flow = 0
        self.density = fuel_density

        # The requested flow rates
        self.outputs = {}
        self.requests = []
        self.requested = 0

        # The owner of this part
        self.spacecraft = None

        # Units of the thing being regulated
        self.unit = unit

    def __str__(self):
        return f'{self.name[:3].lower()} {self.flow:.2e} {self.unit}'

    # Handles one step of simulation
    def reset(self):
        self.outputs = {}
        self.requests = []
        self.requested = 0

    # Adds a request
    def add_request(self, source, amount):
        self.requests.append({'fuel': amount, 'source': source})
        self.requested += amount

    # Pipes fuel into the tank
    def input(self, fuel, source = None, throttle = 1):
        self.flow += fuel * throttle
        if self.flow > self.capacity:
            overflow = self.flow - self.capacity
            self.flow = self.capacity # Ditches excess generation overboard
        
    # Processes the requests
    def process(self, throttle = 1):

        self.sort_requests()

        for request in self.requests:

            request['fuel'] *= throttle

            # Updates capacity and determines how much is supplied
            supplied = 0
            if self.flow < request['fuel']:
                supplied = self.flow
                self.flow = 0
            else:
                supplied = request['fuel']
                self.flow -= request['fuel']
            
            if request['fuel'] == 0:
                self.outputs[request['source'].name] = {'percent': 1, 'fuel': 0}
            else:
                self.outputs[request['source'].name] = {'percent': supplied / request['fuel'], 'fuel': supplied}
    
    # Pipes out
    #   The output is as a fraction out of 1 of the request
    def output(self, source):
        return self.outputs[source.name]

    # Sorts requests by priority; highest priority first
    def sort_requests(self):
        self.requests.sort(key = lambda x: x['fuel'])

    # Overload get mass to return the mass of this part plus its fuel
    def get_mass(self):
        return super().get_mass() + self.flow * self.density
    

# A tank is a Regulator that has time dependent production
class Tank(Regulator):
    def __init__(self, name, mass, capacity, fuel_density = 1, unit  = 'kg'):
        super().__init__(name, mass, capacity, fuel_density, unit)

        # Tanks start full
        self.flow = self.capacity

        # A reference to the time step
        self.time_step = 0
    
    def reset(self, time_step):
        super().reset()
        self.time_step = time_step

    def input(self, fuel, source = None, throttle = 1):
        super().input(fuel, source, self.time_step * throttle)

    def process(self):
        return super().process(self.time_step)