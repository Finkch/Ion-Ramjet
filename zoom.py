# Handles zoom

import vector as v

class Zoom:
    def __init__(self, initial_zoom, timer, actors):
        
        # Sets initial zoom
        self.goal = initial_zoom

        # For easy references
        self.timer = timer
        self.actors = actors

        # Sets initial focus
        self.current = 0
        self.focus = self.actors[self.current]

    # Focuses on the next actor
    def next(self):

        # Goes to the next
        self.current += 1

        # Handles the boundaries
        if self.current >= len(self.actors):
            self.current = 0

        # Updates
        self.update_focus()
    
    # Focuses on the previous actor
    def previous(self):

        # Goes to the previous
        self.current -= 1

        # Handles the boundaries
        if self.current < 0:
            self.current = len(self.actors) - 1

        # Updates
        self.update_focus()
    
    # Sets position to be that of the actor
    def update_focus(self):
        self.focus = self.actors[self.current]
