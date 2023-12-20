import pygame

def init_visuals(width, height):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    return screen