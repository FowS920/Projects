#TODO : Do not import has *
from time import *
from threading import *

# @Define   Time class to do everything time related
#
# @Author   Maxime Lagadec
# @Date     1/13/2018
#
class Counter:

    #Variables definition
    iStartTime = 0
    iCounterValue = 0
    iOldCounterValue = 0

    iDelaiStartTime = 0
    iDelaiTime = 0

    bCounterUp = False

    clThreadStarted = Event()
    clThreadEnded = Event()
    clThreadStop = Event()

    # @Define   Initialisation of the class
    #
    def __init__(self):

        self.clThreadStarted.clear()
        self.clThreadEnded.clear()
        self.clThreadStop.clear()

    # @Define   Returns the variable iCounterValue
    #
    # @Return   Current counter timing
    #
    def GetCounterValue(self):

        return self.iCounterValue

    # @Define   Start counter
    #
    def StartCounter(self):

        if not self.bCounterUp:

            t = Thread(target = self.CounterThread)
            t.start()

            while not self.clThreadStarted.is_set():
                pass

            self.bCounterUp = True

    # @Define   Stop counter
    #
    def StopCounter(self):

        if self.bCounterUp:

            self.clThreadStop.set()

            while not self.clThreadEnded.is_set():
                pass

            self.clThreadStarted.clear()
            self.clThreadEnded.clear()
            self.clThreadStop.clear()

            self.bCounterUp = False
        
    # @Define   Reset counter
    #
    def ResetCounter(self):
        
        self.StopCounter()

        self.iStartTime = 0
        self.iCounterValue = 0
        self.iOldCounterValue = 0

    # @Define   Thread that updates counter values
    #
    def CounterThread(self):

        self.iStartTime = time()
        self.iOldCounterValue = self.iCounterValue

        self.clThreadStarted.set()

        while not self.clThreadStop.is_set():

            self.iCounterValue = self.iOldCounterValue + time() - self.iStartTime

        self.clThreadEnded.set()

    # @Define   Create a string out of the current time and returns it
    #
    # @Param    [in] bBinary : True to return a binary string, false to return a string
    #
    # @Return   The time in string or binary depending on parameter bBinary
    #
    # @Note     Example of time : 15h38m16s
    #
    def GetTime(self, bBinary):

        sTime = strftime("%Hh%Mm%Ss", localtime())

        if bBinary:
            return sTime.encode("utf-8")
        else:
            return sTime

    # @Define   Create a string out of the current date and returns it
    #
    # @Param    [in] bBinary : True to return a binary string, false to return a string
    #
    # @Return   The date in string or binary depending on parameter bBinary
    #
    # @Note     Example of date : 12-Sept-2018
    #
    def GetDate(self, bBinary):

        sDate = strftime("%d-%b-%Y", localtime())

        if bBinary:
            return sDate.encode("utf-8")
        else:
            return sDate