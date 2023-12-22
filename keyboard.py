# This class handles keyboard inputs
import pygame

class Keyboard:
    def __init__(self, timer, zoom, crafts):
        self.timer = timer
        self.zoom = zoom
        self.crafts = crafts

        # Allows key status to be better tracker; keys can be held for multiple inputs
        self.keys = {
            'up':           {'count': 0, 'key': pygame.K_UP,           'type': None,    'function': None}, 
            'down':         {'count': 0, 'key': pygame.K_DOWN,         'type': None,    'function': None}, 
            'right':        {'count': 0, 'key': pygame.K_RIGHT,        'type': None,    'function': None}, 
            'left':         {'count': 0, 'key': pygame.K_LEFT,         'type': None,    'function': None}, 
            'return':       {'count': 0, 'key': pygame.K_RETURN,       'type': None,    'function': None}, 
            'rshift':       {'count': 0, 'key': pygame.K_RSHIFT,       'type': None,    'function': None}, 
            'quote':        {'count': 0, 'key': pygame.K_QUOTE,        'type': None,    'function': None}, 
            'slash':        {'count': 0, 'key': pygame.K_SLASH,        'type': None,    'function': None}, 
            'semicolon':    {'count': 0, 'key': pygame.K_SEMICOLON,    'type': None,    'function': None}, 
            'period':       {'count': 0, 'key': pygame.K_PERIOD,       'type': None,    'function': None}, 
        }

        # Parameters for repeated inputs on button being held down
        self.delay = 45
        self.repeat = 5

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

        if self.pressed('semicolon'):
            self.zoom.increase_order()

        if self.pressed('period'):
            self.zoom.decrease_order()

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
        if keys[self.keys[key]['key']]:
            self.keys[key]['count'] += 1
        else:
            self.keys[key]['count'] = 0
    
    # Returns true so long as the button is held
    def held(self, key):
        return self.keys[key]['count'] >= 1

    # Returns True intermittently, allowing for easy small changes
    def pressed(self, key):
        return self.keys[key]['count'] == 1 or (self.keys[key]['count'] >= self.delay and self.keys[key]['count'] % self.repeat == 0)
    
