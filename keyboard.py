# This class handles keyboard inputs
import pygame

class Keyboard:
    def __init__(self, timer, crafts):
        self.timer = timer
        self.crafts = crafts

        # Allows key status to be better tracker; keys can be held for multiple inputs
        self.keys = {
            'up': {'count': 0, 'type': pygame.K_UP}, 
            'down': {'count': 0, 'type': pygame.K_DOWN}
        }

        # Parameters for repeated inputs on button being held down
        self.delay = 45
        self.repeat = 5


    # Handles accepting input and performing an action
    def __call__(self):

        # Polls currently pressed keys
        self.held_keys()
        

        # Looks through pygame events
        for event in pygame.event.get():
            
            # Looks for a quit event
            if event.type == pygame.QUIT:
                return False
            
            # Hanldes specific key events
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            

        # Handles inputs
        if self.held('up'):
            self.timer.faster()

        if self.held('down'):
            self.timer.slower()
            


        # Returns simulation status
        return True

    # Update keys held
    def held_keys(self):
        keys = pygame.key.get_pressed()
        
        self.update_key(keys, 'up')
        self.update_key(keys, 'down')


    # Updates a key's held-down count
    def update_key(self, keys, key):
        if keys[self.keys[key]['type']]:
            self.keys[key]['count'] += 1
        else:
            self.keys[key]['count'] = 0
    
    # Gets whether holding down a key should return True
    def held(self, key):
        return self.keys[key]['count'] == 1 or (self.keys[key]['count'] >= self.delay and self.keys[key]['count'] % self.repeat == 0)
