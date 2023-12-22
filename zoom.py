# Handles zoom

import vector as v

class Zoom:
    def __init__(self, initial_zoom, timer, actors, position = v.Vector()):
        
        # Sets initial zoom
        self.goal = initial_zoom

        # For easy references
        self.timer = timer
        self.actors = actors

        # Sets initial focus
        self.focus = 0
        self.focus_at(position)

    # Focuses on the next actor
    def next(self):

        # Goes to the next
        self.focus += 1

        # Handles the boundaries
        if self.focus >= len(self.actors):
            self.focus = 0

        # Updates
        self.update_focus()
    
    # Focuses on the previous actor
    def previous(self):

        # Goes to the previous
        self.focus -= 1

        # Handles the boundaries
        if self.focus < 0:
            self.focus = len(self.actors) - 1

        # Updates
        self.update_focus()
    
    # Sets position to be that of the actor
    def update_focus(self):
        self.focus_at(self.actors[self.focus].pos())

    # Focuses at a particular vector
    def focus_at(self, position = v.Vector()):
        self.position = position
