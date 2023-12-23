# Handles zoom

import clock as cl
import constants as c
import numpy as np


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

        self.auto_scale = initial_zoom == 0

    def __call__(self):
        if self.auto_scale:

            # Calculates the max distance between the focus and all actors
            max_distance = max([(self.focus.pos() - actor.pos()).hypo() for actor in self.actors])

            # The max distance is used to set the zoom
            self.set_order(max_distance * 1.2)

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
    



# Handles time and steps
class Time(Orders):
    def __init__(self, rate, goal):
        
        # Simulation steps taken
        self.steps = 0
        
        # Tracks simulation time
        self.sim_time = 0

        # Tracks actual uptime
        self.real_time = cl.Clock(goal)

        # Does the work of ensuring the system stays on track;
        # Handles real-time to sim-time conversion
        self.timer = cl.DynamicClock(rate)

        # If the simulation is paused
        self.paused = False

        # Sets the orders
        super().__init__(rate)

    # Calling this class steps forward once
    def __call__(self):
        time = self.timer.time()
        self.steps += 1
        self.sim_time += time

        return time
    
    # Converts time to a human-readable format
    def __str__(self):
        time = int(self.sim_time)

        return "{years:.2e} y, {days:03} d, {hours:02} h, {minutes:02} m, {seconds:02} s".format(
            years = time // c.year,
            days = (time // c.day) % 365,
            hours = (time // c.hour) % 24,
            minutes = (time // c.minute) % 60,
            seconds = time % 60
        )
    
    # Returns the current rate
    def rate(self):
        return self.get_order()

    # Updates the rate and sets the goal
    def update_rate(self):
        self.timer.change_goal(self.rate())
        self.paused = False
    
    # Increases the simulatoin rate
    def faster(self):

        # Increases rate
        self.increase()

        # Updates the rate
        self.update_rate()
    
    # Significantly increases the goal
    def fasterer(self):
        self.increase_order()
        self.update_rate()

    # Descreases the simulation rate
    def slower(self):
        
        # Decreases rate
        self.decrease()

        # Updates the rate
        self.update_rate()

    # Significantly decreases the goal
    def slowerer(self):
        self.decrease_order()
        self.update_rate()

    # Toggles pause
    def pause(self):
        self.paused = not self.paused
        
        # Updates the goal so sim-time doesn't increase when paused
        if self.paused:
            self.timer.goal = 0
        else:
            self.update_rate()

    # Gets a string prinout
    def get_printout(self):
        return [
            str(self),
            f'{self.rate():.0e}x',
            'Paused' if self.paused else ''
        ]

