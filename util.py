# Several helpful utility functions
import numpy as np
import vector as v

# Returns the hypotenuse of a vector
def hypo(vec):

    # Sums the squares of each component and returns their square root
    hypo = 0
    for component in vec():
        hypo += component ** 2
    return np.sqrt(hypo)


# Returns the theta component of the radial vector
def theta(vec):

    # theta = arccos(z / r)
    return np.arccos(vec.z / hypo(vec))

# Returns the phi component of the radial vector
def phi(vec):

    # phi = sgn(y) * arccos(x / rho)
    return np.sign(vec.y) * np.arccos(vec.x / hypo(v.vector(vec.x, vec.y)))


# Splits a radial vector into its cartesian components.
# It is assumed that vec is a vector with the same orientation
# but a different magnitude
def radial_to_cartesian(radial, theta, phi):
    return v.vector(
        radial * np.sin(theta) * np.cos(phi),
        radial * np.sin(theta) * np.sin(phi),
        radial * np.cos(theta)
    )

# Converts time to a human-readable format
def readable_time(time):
    time = int(time)
    return "{years:.0e} y, {days} d, {hours} h, {minutes} mi, {seconds} s".format(
        years = time // 3.154e+7,
        days = (time // 86400) % 365,
        hours = (time // 3600) % 24,
        minutes = (time // 60) % 60,
        seconds = time % 60
    )


# Calculates the diference between vectors
def dif(a, b):
    return hypo(a - b)