
# A little simulation to play with ion ramjets

# Todo:
#   Create tests
#   Refactor Spacecraft for new parts
#   Build out parts in storage
#   Allow Generator.produce() to have variable efficiency
#   Allows refund overflow to carry up the chain
#   Refactor request-produce?
#       Only call generate on the lowest component
#       Requests carry upward
#       Regulators request until they are full
#       Make Generators a superclass of Regulator?
#           This would mean no Regulators, only Generators talking

# Current branch structure:
#   main
#       spacecraft-parts
#           spacecraft-assembly
#               (soon) refactor


import vector as v
import gravity as g
import visuals as vis
import keyboard as kb
import orders as o
import storage as st

# Should debug printout
DEBUG = False

# First, there was nothing.
# Then, there was "setup".
def setup():

    # Hanldes real-time and sim-time
    #   Initial simulation rate
    #   Framerate
    timer = o.Time(1, 1000 / 60)


    # Sets up the visuals
    screen = vis.init_visuals(768, 768)


    # Grabs the actors
    craft = st.spacecrafts('S-IVB')
    #actors = [st.stars('Sol'), craft]
    actors = [craft]
    
    craft.spacetime.velocity = v.Vector()

    zoom = o.Zoom(0, timer, actors)
    keybboard = kb.Keyboard(timer, zoom, actors, craft)

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
            
            # Draws the screen
            vis.draw(screen, actors, timer, zoom)

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
