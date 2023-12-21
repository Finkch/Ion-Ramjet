# Handles time

class time:
    def __init__(self, step):
        self.step = step
        self.time = 0

        self.orders = ['mus', 'ms', 's', 'min', 'hour', 'day', 'year']
        self.greater_orders = 0

    # Calling this class steps forward once
    def __call__(self):
        self.time += self.step
        return self.step
    
    def faster(self):
        pass

    def slower(self):
        pass