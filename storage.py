# This is a place to store data, such as spacecrafts or planets


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
        