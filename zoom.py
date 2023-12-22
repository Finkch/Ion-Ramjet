# Handles zoom

import vector as v

class Zoom:
    def __init__(self, initial_zoom, focus):
        self.goal = initial_zoom
        
        self.update_focus(focus)

    def update_focus(self, focus):
        if isinstance(focus, v.Vector):
            self.focus = None
            self.pos = focus
        else:
            self.focus = focus
            self.pos = focus.pos()