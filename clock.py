# Handles time for framerate
import time as t

class Clock:
    def __init__(self, goal = -1, length = 10):

        # Gets the start time
        self.start = self()

        # Two initial pushes prevent peek errors
        self.time_stamps = [self.start for i in range(length)]
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

        # Inserts the difference
        self.difs.insert(0, time - self.time_stamps[0])

        # Pushes item to the front
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

    def change_goal(self):

        # Removes all stamps but the most recent
        self.time_stamps = self.time_stamps[:1]
        self.difs = self.difs[:1]

    # Returns the correct amount of simulation time to match the goal's pace
    def time(self):
        self.stamp()

        # Mean time per simulation step in seconds
        self.average_fps = sum(self.difs) / len(self.difs) / 1000

        if self.average_fps == 0:
            return 0

        return self.goal * self.average_fps
    


# Handles time and steps
class time:
    def __init__(self, rate):
        
        # Simulation steps taken
        self.steps = 0
        
        # Tracks simulation time
        self.sim_time = 0

        # Tracks actual uptime
        self.real_time = Clock()

        # How many times faster than real time it should simulate
        self.rate = rate

        # Does the work of ensuring the system stays on track;
        # Handles real-time to sim-time conversion
        self.timer = DynamicClock(rate)

    # Calling this class steps forward once
    def __call__(self):
        time = self.timer()
        self.steps += 1
        self.time += time

        return time
    
    def faster(self):
        pass

    def slower(self):
        pass

