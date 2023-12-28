# Some constants, before they're pushed to the shared lib

import numpy as np

e_0 = 8.8541878128e-12 # F / m
mu_0 = 1.25663706212e-12 # N / A^2

k_e = 1 / (4 * np.pi * e_0) # m / F
k_m = mu_0 / (4 * np.pi)    # N / A^2