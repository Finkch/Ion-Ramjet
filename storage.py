# This is a place to store data, such as spacecrafts or planets

from spacecraft import *
from constants import *

# GENERATORS
def thrusters(name, kwargs = {}):
    match name:
        case 'MPDT-thruster':
            return Generator(name, 10, 26.3, {'p': 5.41073908927e-4, 'e': 750e3}, 'N')
        case 'J-2': # Used on the S-IVB, the upper stage of the Saturn V
            return Generator(name, 1800, 1033e3, {'LOX-LH2': 250.4}, 'N')
        case 'NSTAR':
            return Generator(name, 8.33, 0.092, {'p': 0.000002844774273, 'e': 2.3e3}, 'N') # v_e of 16 660 - 32 340, depending on power supplied
        case _:
            return Tank(name, kwargs['mass'], kwargs['rate'], kwargs['fuel'], unit = 'N')
        
def ionizers(name, kwargs = {}):
    match name:
        case 'MPDT-ionizer':
            return Generator(name, 5, 5.411e-4, {'H': 5.41073908927e-4, 'e': 750e3})
        case _:
            return Tank(name, kwargs['mass'], kwargs['rate'])

def scoops(name, kwargs = {}):
    match name:
        case 'MPDT-scoop':
            return Scoop(name, 5, vacuum_H_mass_density, 100e3, {'e': 750e3})
        case 'Magic Scoop':
            return Generator(name, 5, 1e10)
        case 'Lesser Magic Scoop':
            return Generator(name, 5, 50)
        case _:
            return Tank(name, kwargs['mass'], kwargs['rate'])
        
def reactors(name, kwargs = {}):
    match name:
        case 'MPDT-reactor':
            #return Generator(name, 10, 1.5e6)
            return Generator(name, 10, 1e10, unit = 'W')
        case 'MMRTG': # Used on Perseverence and Curiosity!
            return Generator(name, 45, 110, unit = 'W')
        case 'GPHS-RTG': # Used on many satelites; best W/kg of RTGs
            return Generator(name, 57, 300, unit = 'W')
        case _:
            return Tank(name, kwargs['mass'], kwargs['rate'], unit = 'W')
        
def solar_panels(name, kwargs = {}):
    match name:
        case 'Dawn Solar Array':
            return SolarPanel(name, 0, 0.592) # Assume mass is in the core
        case _:
            return SolarPanel(name, kwargs['mass'], kwargs['efficiency'])
        


# REGULATORS
def tanks(name, kwargs = {}):
    match name:
        case 'hTank-MPDT':
            return Tank(name, 5, 5)
        case 'pTank-MPDT':
            return Tank(name, 5, 5)
        case 'S-IVB Tank':
            return Tank(name, 11.7e3, 109e3)
        case _:
            return Tank(name, kwargs['mass'], kwargs['capacity'])

def batteries(name, kwargs):
    match name:
        case 'eTank-MPDT':
            return Regulator(name, 5, 1e10, 0, 'J/s')
        case _:
            return Tank(name, kwargs['mass'], kwargs['capacity'], 0, 'J')
        



# SPACECRAFT
def spacecrafts(name):
    match name:
        case 'ioRam-0':

            hTank = tanks('hTank-MPDT')
            pTank = tanks('pTank-MPDT')
            battery = batteries('eTank-MPDT')

            thruster = thrusters('MPDT-thruster')
            thruster.link_input(pTank, 'p')
            thruster.link_input(battery, 'e')

            ionizer = ionizers('MPDT-ionizer')
            ionizer.link_input(hTank, 'H')
            ionizer.link_input(battery, 'e')
            ionizer.link_output(pTank)


            scoop = scoops('MPDT-scoop')
            scoop.link_input(battery, 'e')
            scoop.link_output(hTank)

            reactor = reactors('MPDT-reactor')
            reactor.link_output(battery)

            craft = Spacecraft('ioRam-0', 3, 5, 
                               {'ionizer': ionizer, 'scoop': scoop, 'reactor': reactor}, 
                               {'hTank': hTank, 'pTank': pTank, 'eTank': battery}, 
                               thruster)
            return craft
        
        case 'MPDT-sat':
            pTank = tanks('pTank-MPDT')
            eTank = batteries('eTank-MPDT')

            reactor = reactors('MPDT-reactor')
            reactor.link_output(eTank)


            thruster = thrusters('MPDT-thruster')
            thruster.link_input(pTank, 'p')
            thruster.link_input(eTank, 'e')

            craft = Spacecraft('MPDT-sat', 2, 10, {'reactor': reactor}, {'eTank': eTank, 'pTank': pTank}, thruster)

            return craft
        
        case 'S-IVB':

            thruster = thrusters('J-2')
            tank = tanks('S-IVB Tank')

            thruster.link_input(tank, 'LOX-LH2')

            craft = Spacecraft('S-IVB', 18, 0, {}, {'S-IVB Tank': tank}, thruster)
            craft.spacetime.position = v.Vector(au, 0, 0)
            craft.spacetime.velocity = v.Vector(0, au_speed, 0)

            return craft
        
        case 'Dawn':

            tank = tanks('pTank Dawn', {'mass': 0, 'capacity': 470.6})
            battery = batteries('Battery Dawn', {'mass': 0, 'capacity': 4233600})

            solar = solar_panels('Dawn Solar Array')
            solar.link_output(battery)

            thruster = thrusters('NSTAR')
            thruster.link_input(tank, 'p')
            thruster.link_input(battery, 'e')

            # Holy hell, this craft can burn for five years straight!
            # ...and that's for ∆v = 15 km/s
            craft = Spacecraft('Dawn', 1.7, 747.1, {'solar array': solar}, {'pTank': tank, 'eTank': battery}, thruster)

            return craft



# STARS
def stars(name):
    match name:
        case 'Sol':
            return Star(name, sun_mass, sun_radius, L)
        case 'Alpha Centauri A':
            return Star(name, 1.0788 * sun_mass, 1.2175 * sun_radius, 1.5059 * L)
        case 'Alpha Centauri B':
            return Star(name, 0.9092 * sun_mass, 0.8591 * sun_radius, 0.4981 * L)
    
        

# PLANETS
def planets(name):
    match name:
        case 'Terra':
            return None



def universes(name, kwargs):
    match name:
        case 'Basic':

            craft = spacecrafts('ioRam-0')

            craft.spacetime.position = v.Vector(au, 0, 0)
            craft.spacetime.velocity = v.Vector(0, au_speed, 0)

            sol = stars('Sol')

            return [sol, craft], craft

        case 'To Alpha Centauri':
            
            craft = spacecrafts('ioRam-0')

            sol = stars('Sol')
            aca = stars('Alpha Centauri A')
            acb = stars('Alpha Centauri B')


            craft.spacetime.position = v.Vector(10 * au, 0, 0)

            sol.spacetime.position = v.Vector() # Sol is at 0
            

            aca.spacetime.position = v.Vector(ly * d_alpha_centauri, 0, 0)
            acb.spacetime.position = v.Vector(ly * d_alpha_centauri, a_ac, 0)

            acb.spacetime.velocity = v.Vector(-alpha_centauri_velocity * 8.75, 0, 0)

            return [sol, craft, aca, acb], craft
        
    match name:
        case "Alpha Centauri":

            # Sets up the craft
            craft = spacecrafts('ioRam-0')
            craft.spacetime.position = v.Vector(au, 0, 0)
            craft.spacetime.velocity = v.Vector(0, au_speed, 0)

            # Creats the stars
            aca = stars('Alpha Centauri A')
            acb = stars('Alpha Centauri B')

            # Places the stars
            aca.spacetime.velocity = v.Vector(0, 0, 0)
            acb.spacetime.velocity = v.Vector(0, -alpha_centauri_velocity * 8.75, 0)

            acb.spacetime.position = v.Vector(a_ac, 0, 0)

            return [craft, aca, acb], craft
        
        case 'Vacuum':

            craft = spacecrafts(kwargs['craft'])

            return [craft], craft
        