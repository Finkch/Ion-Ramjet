# Handles time for framerate
import time as t

class clock:
    def __init__(self, goal = -1, compensate = False, length = 2):

        # Gets the start time
        self.start = self()

        # Two initial pushes prevent peek errors
        self.time_stamps = [self.start] + [0 for i in range(length - 1)]

        # The goal to aim for
        self.goal = goal

        # Tracks whether to compensate from previous frames
        self.compensate = compensate
    
    # Returns the current time (in ms)
    def __call__(self):
        return t.time_ns() / 1000000

    # Pushes the current time to the queue
    def stamp(self):

        # Pushes item to the front
        self.time_stamps.insert(0, self())

        # Prevents the list from growing too long
        self.time_stamps.pop(-1)

    # Looks at the most recent item
    def peek(self, i = 0):
        return self.time_stamps[i]
    
    # Look at the difference between the most recent two
    def peek_dif(self):
        return self.peek(0) - self.peek(1)

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
        if not self.compensate:
            hit_goal = self.elasped(self.goal)
        else:
            hit_goal = self.elasped(self.goal - self.overtime())

        # If the goal was hit, perform a timestamp
        if hit_goal:
            self.stamp()

        # Returns whether the goal was hit
        return hit_goal
    
    # Returns the difference between the timestamp and the goal
    #   Despite the name, also is the undertime
    def overtime(self):
        return self.peek_dif() - self.goal
