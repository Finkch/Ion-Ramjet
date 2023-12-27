
# A little simulation to play with ion ramjets

# Todo:
#   Create tests

import finkchlib.vector as v
import gravity as g
import visuals as vis
import finkchlib.orders as o
import storage as st
import finkchlib.constants as c
import keyboard as kb

# Should debug printout
DEBUG = False

# First, there was nothing.
# Then, there was "setup".
def setup():

    # Hanldes real-time and sim-time
    #   Initial simulation rate
    #   Framerate
    clock = o.Time(1, 1000 / 60)
    clock.pause()


    # Grabs the actors
    kwargs = {'craft': 'Dawn', 'craft_distance': 13 * c.au, 'craft_speed': 0}
    actors, craft = st.universes('To Alpha Centauri', kwargs)


    screen = vis.IonRamjetDraw(768, 768)
    zoom = o.Zoom(0, clock, actors)
    keyboard = kb.IonRamjetKeyboard(clock, zoom, actors, craft)

    # Simulates
    exist(clock, zoom, screen, keyboard, actors, craft)



# Simulates
def exist(clock, zoom, screen, keyboard, actors, craft):

    # Keeps track of simulation duration
    simulate = True


    # Simulates a workload for a moment to normalise the timer
    clock.real_time.stamp()
    while clock.real_time.dif() < 100:
        clock.timer.time()
        g.easy_gravity(actors)
        for actor in actors:
            actor.spacetime.acceleration = v.Vector()

    # Simulates
    while simulate:

        # Gets the sim time for this step
        time_step = clock()


        # Performs one stpe
        if not clock.paused:
            step(time_step, actors)

            # Debug printout
            debug(clock, craft)

        # Handles an input/draw frame
        if clock.real_time.time():

            # Updates zoom, if necessary
            zoom()
            
            #def __call__(self, zoom, clock, actors, kwargs):
            # Draws the screen
            screen(clock, zoom, actors, {'craft': craft})

            # Handles keyboard inputs
            simulate = keyboard()





# One step of simulation
def step(time_step, actors):

    # Applies gravity
    g.easy_gravity(actors)

    # Simulates each actor
    for actor in actors:
        actor(time_step)


# Performs a debug readout
def debug(clock, craft):

    if not DEBUG:
        return

    print("\n\n" + str(clock))
    print(craft)


# Gets everything going
setup()
