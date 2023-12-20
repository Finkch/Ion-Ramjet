import pygame
import constants as c
from util import *

MIN_SIZE = c.au
MIN_RADIUS = 2
PADDING = 1.2


class shape:
    def __init__(self, radius):
        self.radius = radius
        self.colour = "white"



def init_visuals(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    return screen

# Draws everything
#   focus is the actor at the centre of the display
def draw(screen, focus, actors):
    
    # Clears screen to black
    screen.fill("black")

    # Calculates the scale using the greates seperation distance to the focus
    max_distance = max([abs(dif(focus.pos(), actor.pos())) for actor in actors])
    if max_distance < MIN_SIZE:
        max_distance = MIN_SIZE

    # Finds the maximum distance between the crafts and the PoR.
    # This distance is used to scale everything to fit on screen.
    # Extra factor of two is for half the screen
    scale = screen.get_width() / (max_distance * PADDING) / 2


    draw_actors(screen, actors)

    # Draws?
    pygame.display.flip()
    

# Draws the actors
def draw_actors(screen, focus, actors, scale):
    # Draws each actor
    for actor in actors:

        # Scales the radius a bit; enforces minimum radius
        radius = actor.shape.radius * np.log10(actor.shape.radius) * scale
        if radius < MIN_RADIUS:
            radius = MIN_RADIUS


        # Draws the shape
        pixel_position = (((actor.pos() - focus.pos()) * scale) + v.vector(screen.get_width() / 2, screen.get_height() / 2, 0)).plane()
        pygame.draw.circle(screen, "white", pixel_position, radius)    