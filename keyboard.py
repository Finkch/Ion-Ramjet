from finkchlib.keyboard import Keyboard, Key
import pygame

# A keyboard class for this specific project
class IonRamjetKeyboard(Keyboard):
    def __init__(self, clock, zoom, actors, craft):
        super().__init__()

        self.clock = clock
        self.zoom = zoom
        self.actors = actors
        self.craft = craft

        # Adds the rest of the keys
        self.keys = self.keys | {            
            'up':           Key(pygame.K_UP,        self.clock.fasterer,                'pressed'),
            'down':         Key(pygame.K_DOWN,      self.clock.slowerer,                'pressed'),
            'right':        Key(pygame.K_RIGHT,     self.clock.faster,                  'pressed'), 
            'left':         Key(pygame.K_LEFT,      self.clock.slower,                  'pressed'), 
            'return':       Key(pygame.K_RETURN,    self.zoom.decrease,                 'held'), 
            'rshift':       Key(pygame.K_RSHIFT,    self.zoom.increase,                 'held'), 
            'quote':        Key(pygame.K_QUOTE,     self.zoom.decrease_order,           'pressed'), 
            'slash':        Key(pygame.K_SLASH,     self.zoom.increase_order,           'pressed'), 
            'semicolon':    Key(pygame.K_SEMICOLON, self.zoom.next,                     'pressed'), 
            'period':       Key(pygame.K_PERIOD,    self.zoom.previous,                 'pressed'), 
            'backslash':    Key(pygame.K_BACKSLASH, self.zoom.auto_scale.increase,      'pressed'),
            'a':            Key(pygame.K_a,         self.craft.rotate_ccw,              'held'), 
            'd':            Key(pygame.K_d,         self.craft.rotate_cw,               'held'), 
            'z':            Key(pygame.K_z,         self.craft.throttle.max,            'pressed'), 
            'x':            Key(pygame.K_x,         self.craft.throttle.min,            'pressed'), 
            'c':            Key(pygame.K_c,         self.craft.auto_orient.increase,    'pressed'), 
            'lshift':       Key(pygame.K_LSHIFT,    self.craft.throttle.increase,       'held'), 
            'lcontrol':     Key(pygame.K_LCTRL,     self.craft.throttle.decrease,       'held'),
            }
    
    def __call__(self):

        # Update each key's held status
        super().update_keys()

        # Performs the functions associated with each key
        super().perform_keys()

        # Handle pygame events
        return self.handle_pygame()

    # Overloads Keyboard's pygame event handler
    def handle_pygame(self):

        simulate = True

        # Looks through pygame events
        for event in pygame.event.get():
            
            # Looks for a quit event
            if event.type == pygame.QUIT:
                simulate = False
            
            # Hanldes specific key events
            elif event.type == pygame.KEYDOWN:
                
                # Exits
                if event.key == pygame.K_ESCAPE:
                    simulate = False
                
                # Pauses
                elif event.key == pygame.K_SPACE:
                    self.clock.pause()

        return simulate