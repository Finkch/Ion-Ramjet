# This is a place to store data, such as spacecrafts or planets

from spacecraft import *
from constants import *

# GENERATORS
def thrusters(name):
    match name:
        case 'MPDT-thruster':
            return Generator(name, 10, 26.3, {'p': 5.41073908927e-4, 'e': 750e3})
        case 'J-2': # Used on the S-IVB, the upper stage of the Saturn V
            return Generator(name, 1800, 1033e3, {'LOX-LH2': 250.4})
        
def ionizers(name):
    match name:
        case 'MPDT-ionizer':
            return Generator(name, 5, 5.411e-4, {'H': 5.41073908927e-4, 'e': 750e3})

def scoops(name):
    match name:
        case 'MPDT-scoop':
            return Generator(name, 5, 5.411e-4, {'e': 750e3})
        case 'Magic Scoop':
            return Generator(name, 5, 1e10)
        case 'Lesser Magic Scoop':
            return Generator(name, 5, 50)
        case 'Bussard\'s Scoop':
            return None
        
def reactors(name):
    match name:
        case 'MPDT-reactor':
            #return Generator(name, 10, 1.5e6)
            return Generator(name, 10, 1e10)
        case 'MMRTG': # Used on Perseverence and Curiosity!
            return None
        


# REGULATORS
def tanks(name):
    match name:
        case 'hTank-MPDT':
            return Regulator(name, 5, 500)
        case 'pTank-MPDT':
            return Regulator(name, 5, 500)
        case 'S-IVB Tank':
            return Tank(name, 11.7e3, 109e3)

def batteries(name):
    match name:
        case 'eTank-MPDT':
            return Regulator(name, 5, 1e10, 0, ' J/s')
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

            thruster.consumptions = {
                'LOX-LH2': {
                    'fuel': 250.4,
                    'tank': tank
                }
            }

            craft = Spacecraft('S-IVB', 18, 0, {}, {'S-IVB Tank': tank}, thruster)
            craft.spacetime.position = v.Vector(au, 0, 0)
            craft.spacetime.velocity = v.Vector(0, au_speed, 0)

            return craft



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
        