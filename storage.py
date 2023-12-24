# This is a place to store data, such as spacecrafts or planets

from spacecraft import *
from constants import *

# GENERATORS
def thrusters(name):
    match name:
        case 'MPDT-thruster':
            return None
        
def ionizers(name):
    match name:
        case 'MPDT-ionizer':
            return None

def reactors(name):
    match name:
        case 'MMRTG': # Used on Perseverence and Curiosity!
            return None

def scoops(name):
    match name:
        case 'Bussard\'s Scoop':
            return None
        


# REGULATORS
def tanks(name):
    match name:
        case 'MPDT Hydrogen Tank':
            return None
        case 'MPDT Proton Tank':
            return None

def batteries(name):
    match name:
        case 'Z100':
            return None
        



# SPACECRAFT
def spacecrafts(name):
    match name:
        case 'ioRam-0':
            return None
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
            return None
        

# PLANETS
def planets(name):
    match name:
        case 'Sol':
            return None
        