from finkchlib.keyboard import Keyboard
import pygame

# A keyboard class for this specific project
class IonRamjetKeyboard(Keyboard):
    def __init__(self, timer, zoom, actors, craft):
        super().__init__(timer, zoom, actors)

        self.craft = craft

        # Adds the rest of the keys
        self.keys = self.keys | {            
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