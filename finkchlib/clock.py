# Handles time for framerate
import time as t
import finkchlib.orders as o

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
    

