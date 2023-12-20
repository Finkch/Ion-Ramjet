
# A little simulation to play with ion ramjets

import vector as v
import spacecraft as sc
import time as t
import gravity as g
import constants as c
import util
import pygame
import visuals as vis

# First, there was nothing.
# Then, there was "setup".
def setup():


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
    test_craft.spacetime.velocity = v.vector(0, -c.earth_speed, 0)


    # Simulates
    exist(time_step, [test_craft], screen)



# Simulates
def exist(time_step, crafts, screen):
    
    # Keeps track of timulation time
    time = 0

    # Keeps track of simulation duration
    simulate = True

    # Sun mass
    sun = sc.actor("sun", c.sun_mass, c.sun_radius)
    

    while simulate:

        print("\n\n" + util.readable_time(time))

        # Simulates each craft
        for craft in crafts:
            #craft.force(v.vector(0, craft.mass, 0))
            print("phi:\t{phi:.2f}\ntheta:\t{theta:.2f}".format(phi = util.phi(sun.spacetime.position - craft.spacetime.position), theta = util.theta(sun.spacetime.position - craft.spacetime.position)))
            
            g.easy_gravity([sun], [craft])

            sun(time_step)
            craft(time_step)
            print(craft)

        
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                simulate = False

        vis.draw(screen, sun, [sun, crafts[0]])


        # Keeps track of time
        time += time_step

        # Pauses to make readouts easier to read
        #t.sleep(0.5)

# Gets everything going
setup()
