# Handles zoom

from util import *


# Tracks orders of magnitude and changing between them
class Orders:
    def __init__(self, initial, step_size = 1, digits = 1, minimum = -50, maximum = 150):
        self.step_size = step_size
        self.digits = digits if digits < 9 else 9 # Enforces an upper limit on digits
        self.set_order(initial)
        self.minimum = minimum
        self.maximum = maximum

    # Given a number, extract the scale and the order
    def set_order(self, num):

        # Extracts the leading digits
        self.scale = float(f'{num:.8e}'[:1 if self.digits == 1 else self.digits + 1]) # Accounts for the peroid
        
        # Extracts the order of magnitude
        self.order = int(np.log10(num))

    # Returns the number the order represents
    def get_order(self):
        return self.scale * 10 ** self.order


    # Increases the simulatoin rate
    def increase(self, multiplier = 1):

        # Increases scale
        self.scale += self.step_size * multiplier

        # Hanlde boundry changes
        if self.scale >= 10:
            if self.increase_order():
                self.scale = 1
            else:
                self.scale -= self.step_size * multiplier
            
    
    # Significantly increases the goal
    def increase_order(self):

        # Prevents the order from going above the maximum
        if self.order >= self.maximum:
            self.order = self.maximum
            return False
        
        self.order += 1
        return True

    # Descreases the simulation rate
    def decrease(self, multiplier = 1):
        
        # Descreases scale
        self.scale -= self.step_size * multiplier

        # Handles boundry change
        if self.scale < 1:
            if self.decrease_order():
                self.scale = 10 - self.step_size
            else:
                self.scale = 1

    # Significantly decreases the goal
    def decrease_order(self):

        # Prevents going below the minimum
        if self.order <= self.minimum:
            self.order = self.minimum
            return False
        
        self.order -= 1
        return True


# A linear version of Orders
class Range:
    def __init__(self, initial, step_size = 1, minimum = 0, maximum = 100):
        
        # Sets initial values
        self.scale = initial
        self.step_size = step_size
        self.minimum = minimum
        self.maximum = maximum

    def get(self):
        return self.scale
    
    # Increases the scale
    def increase(self, multiplier = 1):
        self.scale += self.step_size * multiplier

        if self.scale > self.maximum:
            self.scale = self.maximum

    # Decreases the scale
    def decrease(self, multiplier = 1):
        self.scale -= self.step_size * multiplier

        if self.scale < self.minimum:
            self.scale = self.minimum

    # Maximises the scale    
    def max(self):
        self.scale = self.maximum
    
    # Minimises the scale
    def min(self):
        self.scale = self.minimum





class Zoom (Orders):
    def __init__(self, initial_zoom, timer, actors):

        # For easy references
        self.timer = timer
        self.actors = actors

        # Sets initial focus
        self.current = 0
        self.focus = self.actors[self.current]

        # Sets initial zoom
        super().__init__(initial_zoom, 0.05, 3)

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


    # Gets current zoom level
    def zoom(self):
        return self.get_order()
