# Simulates gravity

import constants as c
import util

# Calculates gravitational attraction between all releveant bodies
#   "easy" gravity since we only care about a small set of gravity producers
def easy_gravity(affecters, effectees):
    
    # Returns if the list of affectors is empty
    if len(affecters) == 0:
        return


    # If supplied 1 array, then compute gravity between
    # all items in that array
    if len(effectees) == 0:
        for i in range(len(affecters)):
            for j in range(len(affecter) - i):
                gravity(affecters[i], affecters[j])
    

    # If supplied with 2 arrays, then compute gravity
    # between each pair between the arrays, but not
    # within each array
    for affecter in affecters:
        for effectee in effectees:
            gravity(affecter, effectee)



# Puts gravity from one onto the other
def gravity(a, b):

    position_vector = b.spacetime.position - a.spacetime.position

    # F = G M m / r^2

    # This approach won't work since G is based on the radial component
    force = c.G * a.mass * b.mass / util.hypo(position_vector) ** 2

    # Split the radial vector into the components
    force = util.radial_to_cartesian(force, util.theta(position_vector), util.phi(position_vector))

    # Applies the equal force in opposite directions
    a.force(force)
    b.force(force * -1)