from graphics import *
from util import *
import constants as c

PADDING_PERCENT = 1.2
MIN_SIZE = c.au

# Sets up the screen
def init_visuals(screen_width, screen_height):

    # Creates the screen
    screen = GraphWin("ioRam-0", screen_width, screen_height)
    
    # Sets background colour
    screen.setBackground("black")
    return screen

# Draws the screen
#   por is Point of Reference and is an actor
def draw(screen, por, crafts):

    # Finds the maximum distance between crafts and por
    max_distance = max([dif(por.pos(), craft.pos()) for craft in crafts])

    # Sets the coordinate transform
    xll, yll, xur, yur = get_transform(por, max_distance)
    screen.setCoords(xll, yll, xur, yur)

    # Draws each shape
    por.draw(screen)

    for craft in crafts:
        craft.draw(screen)

def get_transform(por, max_distance):
        
    # Enforces a lower limit on the scale
    if max_distance < MIN_SIZE:
            max_distance = MIN_SIZE
    
    return (por.pos().x - max_distance) * PADDING_PERCENT, (por.pos().y - max_distance) * PADDING_PERCENT, (por.pos().x + max_distance) * PADDING_PERCENT, (por.pos().y + max_distance) * PADDING_PERCENT


class shape:
    def __init__(self, radius):
        self.radius = radius
        self.fill_colour = "white"
        self.outline_colour = "white"

    def __call__(self, position):
        return Circle(Point(position.x, position.y), self.radius)