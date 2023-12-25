# A bunch of constant values
import numpy as np

G =             6.67e-11

year =          3.154e+7
day =           86400
hour =          3600
minute =        60

au =            1.496e11
earth_speed =   29951.68
au_speed =      earth_speed * np.sqrt(2) # Earth speed but it words

sun_mass =      3.995e30
sun_radius =    696340e3

H =             1.6735575e-27

# Number of H per m^3 (100 per cm^3)
vacuum_H_density = 1000000

# Mass of hydrogen per m^3
vacuum_H_mass_density = H * vacuum_H_density