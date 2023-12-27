# Simulates gravity

import finkchlib.constants as c
import finkchlib.vector as v

# Applies gravity between all pairs of actors
def easy_gravity(actors):
    for i in range(len(actors)):
        for j in range(i + 1, len(actors)):
            gravity(actors[i], actors[j])



# Puts gravity from one onto the other
def gravity(a, b):

    position_vector = b.pos() - a.pos()

    # F = G M m / r^2
    force = c.G * a.mass * b.mass / position_vector.hypo() ** 2

    # Split the radial vector into the components
    force = v.radial_to_cartesian(force, position_vector.theta(), position_vector.phi())

    # Applies the equal force in opposite directions
    a.force(force)
    b.force(force * -1)