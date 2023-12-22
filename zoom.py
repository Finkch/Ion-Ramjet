# Handles zoom

import vector as v

class Zoom:
    def __init__(self, initial_zoom, timer, focus = v.Vector()):
        
        # Sets initial zoom
        self.goal = initial_zoom

        # For easy references
        self.timer = timer
        
        # Sets the initial focus
        self.update_focus(focus)


    # Updates the focus of the zoom
    def update_focus(self, focus):
        if isinstance(focus, v.Vector):
            self.focus = None
            self.pos = focus
        else:
            self.focus = focus
            self.pos = focus.pos()