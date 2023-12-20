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
    
    # Sets a global font
    global FONT
    FONT = pygame.font.SysFont('futura', 12)

    return screen


def should_draw(framerate_clock):
    return framerate_clock.time()

# Draws everything
#   focus is the actor at the centre of the display
def draw(screen, focus, actors, framerate_clock):
    

    # Limits the framerate
    if not should_draw(framerate_clock):
        return True



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


    draw_actors(screen, focus, actors, scale)

    # Draws?
    pygame.display.flip()


    # Looks through pygame's events
    return handle_pygame()
    

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

        # Draws labels on each actor
        draw_labels(screen, actor, pixel_position, radius)


# Labels an actor
def draw_labels(screen, actor, pixel_position, radius):

    # Sets up the font
    text = FONT.render(actor.name, True, "white")
    text_shape = text.get_rect()

    # Special angle in a triangle for π/4 radians
    radius_scaled = radius * np.sqrt(1/2) + 2
    
    # The length of the line
    distance = 4

    # Places the label just below the actor
    text_shape.topleft = (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance)

    # Draws the text to screen
    screen.blit(text, text_shape)

    # Draws a line from the text to the actor
    pygame.draw.line(screen, "white", (pixel_position[0] + radius_scaled, pixel_position[1] + radius_scaled), (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance))


# Checks for a quit event
def handle_pygame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True