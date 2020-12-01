"a file contining a timer"

import time

class timer:
    """timer implementation to make timing easear for tests"""
    def __init__(self, acc=1):
        """crate a timer object to keep time for debug pupases
        """
        self.laps = []
        """a list containing the data for all the laps as tupples of type (dtime, msg)"""
        self.startTime = None
        """"a float containing the time on witch the timer was started"""
        self.acc = 1
        """an int conaining how accurate the time is printed in post comma digits"""

    def start(self):
        """starts the the timer
        
        starts timer
        more accuratly it clears laps cach and sets startTime to the current time"""
        self.startTime = time.time()
        self.clear()

    def clear(self):
        "clears laps cach"
        self.laps = []

    def lap(self, msg):
        """add a lap to the timer

        laps are a way to make see how the timings are distributed 
        by giving it a message you can add a tag to the lap
        message
        -------
        the tag of the lap"""
        self.endLap(msg)

    def endLap(self, msg):
        """add a lap to the timer

        laps are a way to make see how the timings are distributed 
        by giving it a message you can add a tag to the lap
        message
        -------
        the tag of the lap"""
        if self.startTime is None:
            raise TimerNotStartedError("u need to start the timer dumbo")
        dt = time.time() - self.startTime
        self.laps.append((dt, msg))
        self.startTime = time.time()

    def end(self, msg='last'):
        """end the timers timing
        
        when this function is called the timer stops running 
        and adds a new lap to the lap cach
        message
        -------
        the tag of the lap"""
        self.endLap(msg)
        self.startTime = None

    def __str__(self):
        """converts type to string"""
        output = ""
        for lap in self.laps:
            output += (f"lap {lap[1]} ended and took {round(lap[0], self.acc)} sec\n")
        return output[:-1]


class TimerNotStartedError(Exception):
    "Errror called when the timer is not startec but should be"
    pass