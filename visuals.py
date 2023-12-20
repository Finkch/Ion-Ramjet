import pygame
import constants as c
from util import *

MIN_SIZE = c.au
PADDING = 1.2


class shape:
    def __init__(self, radius):
        self.radius = radius
        self.colour = "white"



def init_visuals(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    return screen    return screen
