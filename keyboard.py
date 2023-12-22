# This class handles keyboard inputs
import pygame

class Keyboard:
    def __init__(self, timer, zoom, crafts):
        self.timer = timer
        self.zoom = zoom
        self.crafts = crafts

        # Allows key status to be better tracker; keys can be held for multiple inputs
        self.keys = {
            'up': {'count': 0, 'type': pygame.K_UP}, 
            'down': {'count': 0, 'type': pygame.K_DOWN},
            'right': {'count': 0, 'type': pygame.K_RIGHT},
            'left': {'count': 0, 'type': pygame.K_LEFT},
            'return': {'count': 0, 'type': pygame.K_RETURN},
            'rshift': {'count': 0, 'type': pygame.K_RSHIFT},
            'quote': {'count': 0, 'type': pygame.K_QUOTE},
            'slash': {'count': 0, 'type': pygame.K_SLASH},
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
                
                # Exits
                if event.key == pygame.K_ESCAPE:
                    return False
                
                # Pauses
                elif event.key == pygame.K_SPACE:
                    self.timer.pause()
            

        # Handles inputs
        if self.pressed('up'):
            self.timer.faster()

        if self.pressed('down'):
            self.timer.slower()

        if self.pressed('right'):
            self.zoom.next()

        if self.pressed('left'):
            self.zoom.previous()

        if self.held('quote'):
            self.zoom.increase()
        
        if self.held('slash'):
            self.zoom.decrease()

        if self.pressed('return'):
            self.timer.fasterer()

        if self.pressed('rshift'):
            self.timer.slowerer()
            


        # Returns simulation status
        return True

    # Update keys held
    def held_keys(self):
        keys = pygame.key.get_pressed()
        
        # Updates all key status
        for key in self.keys.keys():
            self.update_key(keys, key)


    # Updates a key's held-down count
    def update_key(self, keys, key):
        if keys[self.keys[key]['type']]:
            self.keys[key]['count'] += 1
        else:
            self.keys[key]['count'] = 0
    
    # Returns true so long as the button is held
    def held(self, key):
        return self.keys[key]['count'] >= 1

    # Returns True intermittently, allowing for easy small changes
    def pressed(self, key):
        return self.keys[key]['count'] == 1 or (self.keys[key]['count'] >= self.delay and self.keys[key]['count'] % self.repeat == 0)
    
