import pygame
import constants as c
from util import *
import numpy as np
import spacecraft as sc

MIN_SIZE = c.au
MIN_RADIUS = 2
PADDING = 1.2
PIXEL_PADDING = 10
STRING_PADDING = 18
TYPE_FACE = 'courier'
SMALLER_FONT_SIZE = 12
SMALL_FONT_SIZE = 14
MEDIUM_FONT_SIZE = 16
GREY4 = (255 // 4, 255 // 4, 255 // 4)
GREY2 = (255 // 2, 255 // 2, 255 // 2)

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
    global SMALLER_FONT, SMALL_FONT, MEDIUM_FONT
    SMALLER_FONT = pygame.font.SysFont(TYPE_FACE, SMALLER_FONT_SIZE)
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

    # Draws the reference axis and ticks
    draw_axis(screen)
    draw_scale(screen, max_distance, scale)

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
        pixel_position = (((actor.pos() - focus.pos()) * scale) + v.Vector(WIDTH / 2, HEIGHT / 2, 0)).plane()
        pygame.draw.circle(screen, "white", pixel_position, radius)

        # Draws labels on each actor
        draw_labels(screen, actor, pixel_position, radius)

        # Draws craft's orientation
        if isinstance(actor, sc.Spacecraft):

            # Gets the position of the orientation indicator
            distance = 2
            indicator = (
                    pixel_position[0] + (radius * 3 / 2 + distance) * np.cos(actor.orientation.phi), 
                    pixel_position[1] + (radius * 3 / 2 + distance) * np.sin(actor.orientation.phi)
                )

            pygame.draw.circle(screen, "white", indicator, radius / 2)


# Labels an actor
def draw_labels(screen, actor, pixel_position, radius):

    # Special angle in a triangle for π/4 radians
    radius_scaled = radius * np.sqrt(1/2) + 2
    
    # The length of the line
    distance = 6

    # Renders the name of the actor
    render_text(screen, actor.name, (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance), False, size = "small")

    # Draws a line from the text to the actor
    pygame.draw.line(screen, "white", (pixel_position[0] + radius_scaled, pixel_position[1] + radius_scaled), (pixel_position[0] + radius_scaled + distance, pixel_position[1] + radius_scaled + distance))


# Renders a single bit of text
def render_text(screen, string, position, pad = True, down = True, size = 'medium', colour = 'white', antialias = True, left = True):
    
    # 'Fixes' scientific notation
    string = string.replace("e+", "e")

    # Obtains the font object
    text = None
    if size == 'medium':
        text = MEDIUM_FONT.render(string, antialias, colour)
    elif size == "small":
        text = SMALL_FONT.render(string, antialias, colour)
    else:
        text = SMALLER_FONT.render(string, antialias, colour)
    text_shape = text.get_rect()

    # Gets the correct amount of padding
    padding = PIXEL_PADDING
    if not pad:
        padding = 0

    # Places the text
    if down:
        if left:
            text_shape.topleft = (padding + position[0], padding + position[1])
        else:
            text_shape.topright = (padding + position[0], padding + position[1])
    else:
        if left:
            text_shape.topleft = (padding + position[0], HEIGHT - padding - position[1])
        else:
            text_shape.topright = (padding + position[0], HEIGHT - padding - position[1])

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




# Adds a time readout
def draw_time(screen, sim_time):

    # Sets up the strings to render
    render_text(screen, readable_time(sim_time), [0, 0])


# Adds some of craft information readout
def draw_craft_readout(screen, crafts):
    craft = crafts[0]

    # Sets up the components to render
    strings = [
        craft.name,
        f'phi {craft.orientation.phi:.2f}',
        f'vel {hypo(craft.vel()):.2e} m/s'
    ]

    # Renders the text into a column
    render_text_column(screen, strings, [PIXEL_PADDING, HEIGHT - 2 * PIXEL_PADDING], False)


# Draws two orthogonal lines for the axis
def draw_axis(screen):
    pygame.draw.line(screen, GREY4, (PIXEL_PADDING, HEIGHT / 2), (WIDTH - PIXEL_PADDING, HEIGHT / 2))
    pygame.draw.line(screen, GREY4, (WIDTH / 2, PIXEL_PADDING), (WIDTH / 2, HEIGHT - PIXEL_PADDING))

def draw_scale(screen, max_distance, scale):

    log_scale = int(np.log10(max_distance))
    
    # Iterates over both the current order and within one order
    for order in range(log_scale - 1, log_scale + 1):

        # Iterate over 0 - 10 inclusive
        for i in range(1, 11):

            # Gets the position on the screen offset from the centre
            distance = i * 10 ** order
            x_pos = distance * scale

            # Stop drawing if the x_pos is too large
            if x_pos > WIDTH / 2:
                break

            # Draws the tick
            draw_tick(screen, i, x_pos, distance)
    

    # Draws the current scale
    pygame.draw.line(screen, GREY2, (WIDTH - PIXEL_PADDING, HEIGHT / 2 + 16), (WIDTH - PIXEL_PADDING, HEIGHT / 2 - 16))
    pygame.draw.line(screen, GREY2, (WIDTH / 2 + 16, PIXEL_PADDING), (WIDTH / 2 - 16, PIXEL_PADDING))

    render_text(screen, f'{max_distance:.2e}', (WIDTH - PIXEL_PADDING, HEIGHT / 2 - 32), False, size = 'small', left = False)



def draw_tick(screen, i, x_pos, distance):

    # Gets parameters of the line
    height = 4
    col = GREY2
    text_col = "white"

    cutoff = 0.05
    fade_start = 0.3

    # The multiplier of how solid and large the ticks are
    solid = (x_pos / WIDTH * 2 - cutoff) / fade_start
    
    # Don't draw anything below the cutoff or beyond the edge of the axis
    if solid < 0 or x_pos > WIDTH / 2 - PIXEL_PADDING:
        return
    
    # Fades the attributes
    if solid < 1:
        
        # Obtains the faded text colour
        text_col = 255 * solid
        text_col = (text_col, text_col, text_col)

        # Fades the tick to the axis colour
        #   GREY2 -> GREY4
        col = 127 - 64 * (1 - solid)
        col = (col, col, col)

        # Scales the height of the tick
        height *= solid


    # Offsets the tick towards the centre
    x_pos += WIDTH / 2

    # Draws the major ticks
    if i == 10:
        height *= 3
        render_text(screen, f'{distance:.0e}', (x_pos - 16, HEIGHT / 2 + height + 4), False, size = "smaller", colour = text_col)

    # Draws the minor ticks
    pygame.draw.line(screen, col, (x_pos, HEIGHT / 2 + height), (x_pos, HEIGHT / 2 - height))

    # Draws the ticks on the y-axis
    #   NOTE! Only works if the screen is a square
    pygame.draw.line(screen, col, (HEIGHT / 2 + height, HEIGHT - x_pos), (HEIGHT / 2 - height, HEIGHT - x_pos))


# Checks for a quit event
def handle_pygame():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    return True