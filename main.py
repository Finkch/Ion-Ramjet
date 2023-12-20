
# A little simulation to play with ion ramjets

import vector as v
import spacecraft as sc
import gravity as g
import constants as c
import util
import visuals as vis
import clock

# Should debug printout
DEBUG = False

# First, there was nothing.
# Then, there was "setup".
def setup():

    global framerate
    framerate = clock.clock(1 / 60) # Aim for 60 FPS
    global real_time
    real_time = clock.clock(1 / 60) # Max one sim step per millisecond



    # Sets up the visuals
    screen = vis.init_visuals(512, 512)


    # Important parameters
    time_step = c.day


    # Mass, v_e, F_per, P_per
    test_thruster = sc.thruster(10, 1e3, 1e-27, 1e-23)


    # Mass, P_per, md_in, md_out
    test_ionizer = sc.ionizer(5, 1e-22, 1e20, 1e20)

    # Mass, power, radius
    test_scoop = sc.scoop(10, 1e4, 1e3)

    # Mass, max fuel mass, fuel mass
    test_tank = sc.tank(5, 15, 15)

    # Mass, power
    test_reactor = sc.reactor(10, 1e6)


    # core mass, thruster, ionizer, scoop, tank, reactor
    test_craft = sc.spacecraft("ioRam-0", 5, 5, test_thruster, test_ionizer, test_scoop, test_tank, test_reactor)


    # Some initial movement
    test_craft.spacetime.position = v.vector(c.au, 0, 0)
    test_craft.spacetime.velocity = v.vector(0, c.earth_speed, 0)


    # Simulates
    exist(time_step, [test_craft], screen)



# Simulates
def exist(time_step, crafts, screen):
    
    # Keeps track of timulation time
    time = 0
    steps = 0

    # Keeps track of simulation duration
    simulate = True

    # Sun mass
    sun = sc.actor("sun", c.sun_mass, c.sun_radius)
    

    # Simulates
    while simulate:


        if real_time.time():
            # Performs one stpe
            step(time_step, crafts, [sun])

            # Performs a debug printout
            debug(time, crafts, [sun])

        # Does a step of drawing
        simulate = vis.draw(screen, sun, [sun, crafts[0]], framerate)

        # Tracks uptime
        time += time_step
        steps += 1


# One step of simulation
def step(time_step, crafts, other_actors):

    # Applies gravity
    g.easy_gravity(other_actors, crafts)

    # Simulates each craft
    for craft in crafts:
        craft(time_step)

    # Performs a step of simulation for "linear" actors
    for actor in other_actors:
        actor(time_step)


# Performs a debug readout
def debug(time, crafts, other_actors):

    if not DEBUG:
        return

    print("\n\n" + util.readable_time(time))
    for craft in crafts:
        print(craft)


# Gets everything going
setup()
