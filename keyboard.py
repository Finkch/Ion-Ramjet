from finkchlib.keyboard import Keyboard
import pygame

# A keyboard class for this specific project
class IonRamjetKeyboard(Keyboard):
    def __init__(self, timer, zoom, actors, craft):
        super().__init__()

        self.timer = timer
        self.zoom = zoom
        self.actors = actors
        self.craft = craft

        # Adds the rest of the keys
        self.keys = self.keys | {            
            'up':           {'count': 0, 'key': pygame.K_UP,            'type': self.pressed,       'function': self.clock.fasterer}, 
            'down':         {'count': 0, 'key': pygame.K_DOWN,          'type': self.pressed,       'function': self.clock.slowerer}, 
            'right':        {'count': 0, 'key': pygame.K_RIGHT,         'type': self.pressed,       'function': self.clock.faster}, 
            'left':         {'count': 0, 'key': pygame.K_LEFT,          'type': self.pressed,       'function': self.clock.slower}, 
            'return':       {'count': 0, 'key': pygame.K_RETURN,        'type': self.held,          'function': self.zoom.decrease}, 
            'rshift':       {'count': 0, 'key': pygame.K_RSHIFT,        'type': self.held,          'function': self.zoom.increase}, 
            'quote':        {'count': 0, 'key': pygame.K_QUOTE,         'type': self.pressed,       'function': self.zoom.decrease_order}, 
            'slash':        {'count': 0, 'key': pygame.K_SLASH,         'type': self.pressed,       'function': self.zoom.increase_order}, 
            'semicolon':    {'count': 0, 'key': pygame.K_SEMICOLON,     'type': self.pressed,       'function': self.zoom.next}, 
            'period':       {'count': 0, 'key': pygame.K_PERIOD,        'type': self.pressed,       'function': self.zoom.previous}, 
            'backslash':    {'count': 0, 'key': pygame.K_BACKSLASH,     'type': self.pressed,       'function': self.zoom.auto_scale.increase},
            'w':            {'count': 0, 'key': pygame.K_w,             'type': self.held,          'function': None}, 
            's':            {'count': 0, 'key': pygame.K_s,             'type': self.held,          'function': None}, 
            'a':            {'count': 0, 'key': pygame.K_a,             'type': self.held,          'function': self.craft.rotate_ccw}, 
            'd':            {'count': 0, 'key': pygame.K_d,             'type': self.held,          'function': self.craft.rotate_cw}, 
            'z':            {'count': 0, 'key': pygame.K_z,             'type': self.pressed,       'function': self.craft.throttle.max}, 
            'x':            {'count': 0, 'key': pygame.K_x,             'type': self.pressed,       'function': self.craft.throttle.min}, 
            'c':            {'count': 0, 'key': pygame.K_c,             'type': self.pressed,       'function': self.craft.auto_orient.increase}, 
            'lshift':       {'count': 0, 'key': pygame.K_LSHIFT,        'type': self.held,          'function': self.craft.throttle.increase}, 
            'lcontrol':     {'count': 0, 'key': pygame.K_LCTRL,         'type': self.held,          'function': self.craft.throttle.decrease},
            }