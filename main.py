
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
    timer = o.Time(1, 1000 / 60)
    timer.pause()


    # Grabs the actors
    kwargs = {'craft': 'Dawn', 'craft_distance': 13 * c.au, 'craft_speed': 0}
    actors, craft = st.universes('To Alpha Centauri', kwargs)


    screen = vis.IonRamjetDraw(768, 768)
    zoom = o.Zoom(0, timer, actors)
    keybboard = kb.IonRamjetKeyboard(timer, zoom, actors, craft)

    # Simulates
    exist(timer, screen, keybboard, zoom, actors, craft)



# Simulates
def exist(timer, screen, keybboard, zoom, actors, craft):

    # Keeps track of simulation duration
    simulate = True


    # Simulates a workload for a moment to normalise the timer
    timer.real_time.stamp()
    while timer.real_time.dif() < 100:
        timer.timer.time()
        g.easy_gravity(actors)
        for actor in actors:
            actor.spacetime.acceleration = v.Vector()

    # Simulates
    while simulate:

        # Gets the sim time for this step
        time_step = timer()


        # Performs one stpe
        if not timer.paused:
            step(time_step, actors)

            # Debug printout
            debug(timer, craft)

        # Handles an input/draw frame
        if timer.real_time.time():

            # Updates zoom, if necessary
            zoom()
            
            #def __call__(self, zoom, clock, actors, kwargs):
            # Draws the screen
            screen(timer, zoom, actors, {'craft': craft})

            # Handles keyboard inputs
            simulate = keybboard()





# One step of simulation
def step(time_step, actors):

    # Applies gravity
    g.easy_gravity(actors)

    # Simulates each actor
    for actor in actors:
        actor(time_step)


# Performs a debug readout
def debug(timer, craft):

    if not DEBUG:
        return

    print("\n\n" + str(timer))
    print(craft)


# Gets everything going
setup()
