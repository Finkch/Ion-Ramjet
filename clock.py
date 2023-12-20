# Handles time for framerate
import time as t

class clock:
    def __init__(self, goal = -1):

        # Gets the start time
        self.start = self()

        self.time_stamps = [self.start]

        self.goal = goal
    
    # Returns the current time (in ms)
    def __call__(self):
        return t.time_ns() / 1000

    # Pushes the current time to the queue
    def stamp(self):

        # Pushes item to the front
        self.time_stamps.insert(0, self())

        # If the list is too long, pops the last item
        if len(self.time_stamps) > 5:
            self.time_stamps.pop(-1)

    # Looks at the most recent item
    def peek(self):
        return self.time_stamps[0]

    # Returns the time since the previous stamp
    def dif(self):
        return self() - self.peek()
    
    # Checks if the argument's amount of time has passed
    def elasped(self, amount):
        return amount < self.dif()
    
    def time(self):
        hit_goal = self.elasped(self.goal)
        if hit_goal:
            self.stamp()
        return hit_goal
