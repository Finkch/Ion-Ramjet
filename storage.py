# This is a place to store data, such as spacecrafts or planets

from spacecraft import *
from constants import *

# GENERATORS
def thrusters(name):
    match name:
        case 'MPDT-thruster':
            return Generator(name, 10, 26.3)
        case 'J-2': # Used on the S-IVB, the upper stage of the Saturn V
            return Generator(name, 1800, 1033e3)
        
def ionizers(name):
    match name:
        case 'MPDT-ionizer':
            return Generator(name, 5, 5.411e-4)

def scoops(name):
    match name:
        case 'MPDT-scoop':
            return Generator(name, 5, 5.411e-4)
        case 'Magic Scoop':
            return Generator(name, 5, 1e10)
        case 'Bussard\'s Scoop':
            return None
        
def reactors(name):
    match name:
        case 'MPDT-reactor':
            return Generator(name, 10, 1.5e6)
        case 'MMRTG': # Used on Perseverence and Curiosity!
            return None
        


# REGULATORS
def tanks(name):
    match name:
        case 'MPDT-hTank':
            return Regulator(name, 5, 500)
        case 'MPDT-pTank':
            return Regulator(name, 5, 500)
        case 'S-IVB Tank':
            return Regulator(name, 11.7e3, 500)

def batteries(name):
    match name:
        case 'MPDT-battery':
            return Regulator(name, 5, 100, 0)
        case 'Z100':
            return None
        



# SPACECRAFT
def spacecrafts(name):
    match name:
        case 'ioRam-0':
            thruster = thrusters('MPDT-thruster')
            ioniezr = ionizers('MPDT-ionizer')
            scoop = scoops('MPDT-scoop')
            reactor = reactors('MPDT-reactor')

            hTank = tanks('MPDT-hTank')
            pTank = tanks('MPDT-pTank')
            battery = batteries('MPDT-battery')

            craft = Spacecraft()
            return None
        
        case 'S-IVB':

            thruster = thrusters('J-2')
            tank = tanks('S-IVB Tank')
            scoop = scoops('Magic Scoop')

            scoop.tank = tank

            thruster.consumptions = {
                'LOX-LH2': {
                    'fuel': 250.4,
                    'tank': tank
                }
            }

            craft = Spacecraft('S-IVB', 18, 0, {'Magic Scoop': scoop}, {'S-IVB Tank': tank}, thruster)
            craft.spacetime.position = v.Vector(au, 0, 0)
            craft.spacetime.velocity = v.Vector(0, au_speed, 0)

            return craft

        case 'test_craft': # An outdated model


            # Mass, v_e, F_per, P_per
            test_thruster = thruster(10, 4.81e4, 26.3, 1e-23)


            # Mass, P_per, md_in, md_out
            test_ionizer = ionizer(5, 1e-22, 1e20, 1e20)

            # Mass, power, radius
            test_scoop = scoop(10, 1e4, 1e3)

            # Mass, max fuel mass, fuel mass
            test_tank = tank(5, 15, 15)

            # Mass, power
            test_reactor = reactor(10, 1e6)


            # core mass, thruster, ionizer, scoop, tank, reactor
            test_craft = Spacecraft("ioRam-0", 5, 5, test_thruster, test_ionizer, test_scoop, test_tank, test_reactor)


            # Some initial movement
            test_craft.spacetime.position = v.Vector(au, 0, 0)
            #test_craft.spacetime.velocity = v.Vector(0, c.au_speed, 0)


            return test_craft




# STARS
def stars(name):
    match name:
        case 'Sol':
            return Actor("sun", sun_mass, sun_radius)
        

# PLANETS
def planets(name):
    match name:
        case 'Sol':
            return None
        