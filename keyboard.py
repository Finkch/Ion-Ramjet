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
            'up':           Key(pygame.K_UP,        self.pressed,   self.clock.fasterer),
            'down':         Key(pygame.K_DOWN,      self.pressed,   self.clock.slowerer),
            'right':        Key(pygame.K_RIGHT,     self.pressed,   self.clock.faster), 
            'left':         Key(pygame.K_LEFT,      self.pressed,   self.clock.slower), 
            'return':       Key(pygame.K_RETURN,    self.held,      self.zoom.decrease), 
            'rshift':       Key(pygame.K_RSHIFT,    self.held,      self.zoom.increase), 
            'quote':        Key(pygame.K_QUOTE,     self.pressed,   self.zoom.decrease_order), 
            'slash':        Key(pygame.K_SLASH,     self.pressed,   self.zoom.increase_order), 
            'semicolon':    Key(pygame.K_SEMICOLON, self.pressed,   self.zoom.next), 
            'period':       Key(pygame.K_PERIOD,    self.pressed,   self.zoom.previous), 
            'backslash':    Key(pygame.K_BACKSLASH, self.pressed,   self.zoom.auto_scale.increase),
            'a':            Key(pygame.K_a,         self.held,      self.craft.rotate_ccw), 
            'd':            Key(pygame.K_d,         self.held,      self.craft.rotate_cw), 
            'z':            Key(pygame.K_z,         self.pressed,   self.craft.throttle.max), 
            'x':            Key(pygame.K_x,         self.pressed,   self.craft.throttle.min), 
            'c':            Key(pygame.K_c,         self.pressed,   self.craft.auto_orient.increase), 
            'lshift':       Key(pygame.K_LSHIFT,    self.held,      self.craft.throttle.increase), 
            'lcontrol':     Key(pygame.K_LCTRL,     self.held,      self.craft.throttle.decrease),
            }