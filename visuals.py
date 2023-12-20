import pygame
import constants as c
from util import *

MIN_SIZE = c.au
MIN_RADIUS = 2
PADDING = 1.2
PIXEL_PADDING = 10
STRING_PADDING = 18
TYPE_FACE = 'courier'
SMALL_FONT_SIZE = 12
MEDIUM_FONT_SIZE = 16


# Holds some basic information on how to draw an object
class shape:
    def __init__(self, radius):
        self.radius = radius
        self.colour = "white"



# Prepares the graphics
def init_visuals(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))

    # Sets global screen size
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height
    
    # Sets a global font
    global SMALL_FONT, MEDIUM_FONT
    SMALL_FONT = pygame.font.SysFont(TYPE_FACE, SMALL_FONT_SIZE)
    MEDIUM_FONT = pygame.font.SysFont(TYPE_FACE, MEDIUM_FONT_SIZE)

    return screen


# Checks whether enough time has passed to perform a draw
def should_draw(framerate_clock):
    return framerate_clock.time()



# Draws everything
#   focus is the actor at the centre of the display
def draw(screen, focus, actors, framerate_clock, sim_time):
    
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
    scale = WIDTH / (max_distance * PADDING) / 2


    # Draws the actors to screen
    draw_actors(screen, focus, actors, scale)

    # Adds a readout for the current sim time
    draw_time(screen, sim_time)

    # Draws some craft informatiom
    draw_craft_readout(screen, [actors[1]])

    # Draws
    pygame.display.flip()

    # Looks through pygame's events
    #   Used only for game_exit
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
        pixel_position = (((actor.pos() - focus.pos()) * scale) + v.vector(WIDTH / 2, HEIGHT / 2, 0)).plane()
        pygame.draw.circle(screen, "white", pixel_position, radius)

        # Draws labels on each actor
        draw_labels(screen, actor, pixel_position, radius)


# Labels an actor
def draw_labels(screen, actor, pixel_position, radius):

    # Sets up the font
    text = SMALL_FONT.render(actor.name, True, "white")
    text_shape = text.get_rect()

    # Special angle in a triangle for π/4 radians
    radius_scaled = radius * np.sqrt(1/2) + 2
    
    # The length of the line
    distance = 6

    # Places the label just below the actor
    text_shape.topleft = (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance)

    # Draws the text to screen
    screen.blit(text, text_shape)

    # Draws a line from the text to the actor
    pygame.draw.line(screen, "white", (pixel_position[0] + radius_scaled, pixel_position[1] + radius_scaled), (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance))

def draw_time(screen, sim_time):

    # Sets up the font
    text = MEDIUM_FONT.render(readable_time(sim_time), True, "white")
# Renders a single bit of text
def render_text(screen, string, position, pad = True, down = True):
    
    # Obtains the font object
    text = MEDIUM_FONT.render(string, True, "white")
    text_shape = text.get_rect()

    # Gets the correct amount of padding
    padding = PIXEL_PADDING
    if not pad:
        padding = 0

    # Places the text
    if down:
        text_shape.topleft = (padding + position[0], padding + position[1])
    else:
        text_shape.topleft = (padding + position[0], HEIGHT - padding - position[1])

    # Renders the text
    screen.blit(text, text_shape)
        

# Renders a column of text in rows as specified by strings
def render_text_column(screen, strings, position, down = True):
    
    # Iterates over all strings
    draw_at = [None, None]
    for i in range(len(strings)):

        # Obtains the position to draw them at
        draw_at[0] = position[0]
        if down:
            draw_at[1] = position[1] + i * STRING_PADDING
        else:
            draw_at[1] = position[1] - (len(strings) - i) * STRING_PADDING + 8
        

        # Renders the text row
        render_text(screen, strings[i], draw_at, down)


def draw_velocity():
    pass

def draw_axis():
    pass

def draw_scale():
    pass

# Checks for a quit event
def handle_pygame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True