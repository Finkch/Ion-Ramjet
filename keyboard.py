# This class handles keyboard inputs
import pygame

class Keyboard:
    def __init__(self, timer, crafts):
        self.timer = timer
        self.crafts = crafts


    # Handles accepting input and performing an action
    def __call__(self):
        keys = pygame.key.get_pressed()
        print(keys)

        # Looks through pygame events
        for event in pygame.event.get():
            
            # Looks for a quit event
            if event.type == pygame.QUIT:
                return False
            
            # Handles keyboard inputs
            if event.type == pygame.KEYDOWN:
                pass
            
        # Returns simulation status
        return True
