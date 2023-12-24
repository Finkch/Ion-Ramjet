
# A little simulation to play with ion ramjets

# Todo:
#   Create tests


import vector as v
import spacecraft as sc
import gravity as g
import constants as c
import visuals as vis
import keyboard as kb
import orders as o

# Should debug printout
DEBUG = False

# First, there was nothing.
# Then, there was "setup".
def setup():

    # Hanldes real-time and sim-time
    #   Initial simulation rate
    #   Framerate
    timer = o.Time(1e5, 1000 / 60)


    # Sets up the visuals
    screen = vis.init_visuals(768, 768)
    

    zoom = o.Zoom(0, timer, crafts)
    keybboard = kb.Keyboard(timer, zoom, crafts)

    # Simulates
    exist(timer, crafts, screen, keybboard, zoom)



# Simulates
def exist(timer, crafts, screen, keybboard, zoom):

    # Keeps track of simulation duration
    simulate = True

    # Sun mass
    sun = sc.Actor("sun", c.sun_mass, c.sun_radius)
    zoom.actors = [sun, crafts[0]]
    zoom.update_focus()


    # Simulates a workload for a moment to normalise the timer
    timer.real_time.stamp()
    while timer.real_time.dif() < 100:
        timer.timer.time()
        g.easy_gravity([sun], crafts)
        sun.spacetime.acceleration = v.Vector()
        for craft in crafts:
            craft.spacetime.acceleration = v.Vector()

    # Simulates
    while simulate:

        # Gets the sim time for this step
        time_step = timer()


        # Performs one stpe
        if not timer.paused:
            step(time_step, crafts, [sun])

            # Debug printout
            debug(timer, crafts, [sun])

        # Handles an input/draw frame
        if timer.real_time.time():

            # Updates zoom, if necessary
            zoom()
            
            # Draws the screen
            vis.draw(screen, [sun, crafts[0]], timer, zoom)

            # Handles keyboard inputs
            simulate = keybboard()





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
def debug(timer, crafts, other_actors):

    if not DEBUG:
        return

    print("\n\n" + str(timer))
    for craft in crafts:
        print(craft)


# Gets everything going
setup()
