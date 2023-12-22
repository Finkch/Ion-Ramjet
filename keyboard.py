# This class handles keyboard inputs
import pygame

class Keyboard:
    def __init__(self, timer, zoom, crafts):
        self.timer = timer
        self.zoom = zoom
        self.crafts = crafts

        # Allows key status to be better tracker; keys can be held for multiple inputs
        self.keys = {
            'up':           {'count': 0, 'key': pygame.K_UP,           'type': self.pressed,    'function': self.timer.fasterer}, 
            'down':         {'count': 0, 'key': pygame.K_DOWN,         'type': self.pressed,    'function': self.timer.slowerer}, 
            'right':        {'count': 0, 'key': pygame.K_RIGHT,        'type': self.pressed,    'function': self.timer.faster}, 
            'left':         {'count': 0, 'key': pygame.K_LEFT,         'type': self.pressed,    'function': self.timer.slower}, 
            'return':       {'count': 0, 'key': pygame.K_RETURN,       'type': self.held,       'function': self.zoom.decrease}, 
            'rshift':       {'count': 0, 'key': pygame.K_RSHIFT,       'type': self.held,       'function': self.zoom.increase}, 
            'quote':        {'count': 0, 'key': pygame.K_QUOTE,        'type': self.pressed,    'function': self.zoom.decrease_order}, 
            'slash':        {'count': 0, 'key': pygame.K_SLASH,        'type': self.pressed,    'function': self.zoom.increase_order}, 
            'semicolon':    {'count': 0, 'key': pygame.K_SEMICOLON,    'type': self.pressed,    'function': self.zoom.next}, 
            'period':       {'count': 0, 'key': pygame.K_PERIOD,       'type': self.pressed,    'function': self.zoom.previous}, 
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
        for key in self.keys.keys():
            if self.keys[key]['type'](key):
                self.keys[key]['function']()
            


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
    
