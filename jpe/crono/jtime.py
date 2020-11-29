import time

class timer:
    def __init__(self, acc=1):
        self.laps = []
        self.startTime = None
        self.acc = 1

    def start(self):
        self.startTime = time.time()
        self.clear()

    def clear(self):
        self.laps = []

    def lap(self, msg):
        self.endLap(msg)

    def endLap(self, msg):
        if self.startTime is None:
            raise TimerNotStartedError("u need to start the timer dumbo")
        dt = time.time() - self.startTime
        self.laps.append((dt, msg))
        self.startTime = time.time()

    def end(self, msg='last'):
        self.endLap(msg)
        self.startTime = None
        print(self)

    def __str__(self):
        output = ""
        for lap in self.laps:
            output += (f"lap {lap[1]} ended and took {round(lap[0], self.acc)} sec\n")
        return output[:-1]


class TimerNotStartedError(Exception):
    pass