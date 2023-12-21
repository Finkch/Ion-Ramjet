# Handles time for framerate
import time as t

class clock:
    def __init__(self, goal = -1, length = 10):

        # Gets the start time
        self.start = self()

        # Two initial pushes prevent peek errors
        self.time_stamps = [self.start for i in range(length)]

        self.length = length

        # The goal to aim for
        self.goal = goal

    
    # Returns the current time (in ms)
    def __call__(self):
        return t.time_ns() / 1000000

    # Pushes the current time to the queue
    def stamp(self, offset = 0):

        # Pushes item to the front
        self.time_stamps.insert(0, self())

        # Prevents the list from growing too long
        self.time_stamps.pop(-1)

    # Looks at the most recent item
    def peek(self, i = 0):
        if i >= self.length:
            return -1
        return self.time_stamps[i]
    
    # Look at the difference between the most recent two
    def peek_dif(self, i = 0):
        if i >= self.length - 1:
            return -1
        return self.peek(i) - self.peek(i + 1)

    # Returns the time since the previous stamp
    def dif(self):
        return self() - self.peek()
    
    # Checks if the argument's amount of time has passed
    def elasped(self, amount):
        return amount < self.dif()

    
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
