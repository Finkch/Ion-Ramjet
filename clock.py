# Handles time for framerate
import time as t
import numpy as np

class Clock:
    def __init__(self, goal = -1, length = 10):

        # Gets the start time
        self.start = self()

        # Two initial pushes prevent peek errors
        self.time_stamps = [self.start]
        self.difs = []

        self.length = length

        # The goal to aim for
        self.goal = goal

    
    # Returns the current time (in ms)
    def __call__(self):
        return t.time_ns() / 1000000

    # Pushes the current time to the queue
    def stamp(self, offset = 0):

        time = self()

        # Pushes item to the front
        self.difs.insert(0, time - self.time_stamps[0])
        self.time_stamps.insert(0, time)
            

        # Prevents the list from growing too long
        if len(self.time_stamps) > self.length:
            self.time_stamps.pop(-1)
            self.difs.pop(-1)

    # Looks at the most recent item
    def peek(self, i = 0):
        if i >= len(self.time_stamps) - 1:
            return -1
        return self.time_stamps[i]
    
    # Look at the difference between the most recent two
    def peek_dif(self, i = 0):
        if i >= len(self.difs) - 1:
            return -1
        return self.difs[i]

    # Returns the time since the previous stamp
    def dif(self):
        return self() - self.peek()
    
    # Checks if the argument's amount of time has passed
    def elasped(self, amount):
        return amount < self.dif()
    
    # Returns the averages of arrays
    def get_average_stamps(self):
        return sum(self.time_stamps) / len(self.time_stamps)

    def get_average_difs(self):
        return sum(self.difs) / len(self.difs)

    
    # Returns true if the time hit was the goal
    #   Performs a timestamp is so
    def time(self):

        # Checks whether we compensate for previous slow frames
        hit_goal = self.elasped(self.goal)

        # If the goal was hit, perform a timestamp
        if hit_goal:
            self.stamp()

        # Returns whether the goal was hit
        return hit_goal
    
    # Returns the difference between the timestamp and the goal
    #   Despite the name, also is the undertime
    def overtime(self):
        return self.peek_dif() - self.goal


# A dynamic clock aims to create some rate (it's goal) based on the frequency of stamps
class DynamicClock(Clock):
    def __init__(self, goal):
        super().__init__(goal, 1) # Converts goal from seconds to milliseconds

        # Starts the average at the goal
        self.average_fps = 0

        # Sets the length so that the stamp array starts with only 1 item
        self.length = 20

    # Changes the current goal of this timer
    def change_goal(self, goal):

        # Updates goal
        self.goal = goal

        # Removes all stamps but the most recent.
        # Different bounds ensures the sizes remain constant
        self.time_stamps = self.time_stamps[:2]
        self.difs = self.difs[:1]

    # Returns the correct amount of simulation time to match the goal's pace
    def time(self):
        self.stamp()

        # Mean time per simulation step in seconds
        return self.goal * self.get_average_difs() / 1000
    


# Handles time and steps
class Time:
    def __init__(self, rate, goal):
        
        # Simulation steps taken
        self.steps = 0
        
        # Tracks simulation time
        self.sim_time = 0

        # Tracks actual uptime
        self.real_time = Clock(goal)

        # Does the work of ensuring the system stays on track;
        # Handles real-time to sim-time conversion
        self.timer = DynamicClock(rate)

        # Allows for easier transitions between rates scales.
        # Sets the initial values based on the rate argument
        self.scale = int(str(rate)[:1])
        self.order = int(np.log10(rate))

        # If the simulation is paused
        self.paused = False

    # Calling this class steps forward once
    def __call__(self):
        time = self.timer.time()
        self.steps += 1
        self.sim_time += time

        return time
    
    # Returns the current rate
    def rate(self):
        return self.scale * 10 ** self.order

    # Updates the rate and sets the goal
    def update_rate(self):
        self.timer.change_goal(self.rate())
        self.paused = False
    
    # Increases the simulatoin rate
    def faster(self):

        # Increases scale
        self.scale += 1

        # Hanlde boundry changes
        if self.scale == 10:
            self.scale = 1
            self.order += 1

        # Updates the rate
        self.update_rate()
    
    # Significantly increases the goal
    def fasterer(self):
        self.order += 1
        self.update_rate()

    # Descreases the simulation rate
    def slower(self):
        
        # Descreases scale
        self.scale -= 1

        # Handles boundry change
        if self.scale == 0:
            self.scale = 9
            self.order -= 1

        # Updates the rate
        self.update_rate()

    # Significantly decreases the goal
    def slowerer(self):
        self.order -= 1
        self.update_rate()

    # Toggles pause
    def pause(self):
        self.paused = not self.paused
        
        # Updates the goal so sim-time doesn't increase when paused
        if self.paused:
            self.timer.goal = 0
        else:
            self.update_rate()
