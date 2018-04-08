from gSettings import *
from cCounter import *

import shutil
import io
import os

# @Define   Log class used to log events
#
# @Author   Maxime Lagadec
# @Date     2/12/2018
#
class Log:

    #Variables definition
    bFileOpen = False       # << Is there a file opened
    bOpenInBinary = False   # << Is the file opened in binary

    #clFile                 # << File used for logging

    sLogFileName = ""       # << Log file name
    sLogFilePosition = ""   # << Log file position

    # @Define   Initialisation of the class
    #
    def __init__(self):

        pass

    # @Define   Destruction of the class
    #
    # @TODO
    #
    def __del__(self):

        self.FileClose()

    # @Define   Setup the log file
    #
    # @Param    [in] sLogFileName : Name of the file
    # @Param    [in] sLogFilePosition : Position of the file
    # @Param    [in] bBinary : True to open in binary, false to open in text
    #
    # @Return   True : Success, False : Error
    #
    def FileSetup(self, sLogFileName, sLogFilePosition, bBinary):

        #Add \\ to make sure we are inside the folder
        sLogFilePosition += "\\"

        sLogFile = sLogFilePosition
        sLogFile += sLogFileName

        #Check if file position is valid
        if not os.path.isdir(sLogFilePosition):
            return False

        #Check if file name is valid
        if sLogFileName.count(".") != 1:
            return False

        if not self.bFileOpen:
            try:
                if bBinary:
                    self.clFile = io.open(sLogFile, "ab+")
                    self.clFile.seek(0, 0)
                else:
                    self.clFile = io.open(sLogFile, "a+")
                    self.clFile.seek(0, 0)
            except:
                return False

        self.bFileOpen = True
        self.bOpenInBinary = bBinary

        self.sLogFileName = sLogFileName
        self.sLogFilePosition = sLogFilePosition

        return True

    # @Define   Close the log file
    #
    # @Return   True : Success, False : Error
    #
    # @Note     File has to be setup in order for this function to work
    #
    def FileClose(self):

        if self.bFileOpen:
            try:
                self.clFile.close()
            except:
                return False

        self.bFileOpen = False
        self.bOpenInBinary = False

        self.sLogFileName = ""
        self.sLogFilePosition = ""

        return True


    # @Define   Reset the current log file
    #
    # @Return   True : Success, False : Error
    #
    # @Note     File has to be setup in order for this function to work
    #
    def FileReset(self):

        if self.bFileOpen:
            try:
                self.clFile.truncate()
            except:
                return False

            return True

        return False

    # @Define   Write to the current log file
    #
    # @Param    [in] LogInput : String to be written to the file
    # @Param    [in] bBinary : True if string is binary, false if text string
    #
    # @Return   True : Success, False : Error
    #
    def Write(self, LogInput, bBinary):

        if self.bFileOpen:

            try:
                if bBinary:
                    if self.bOpenInBinary:
                        NewLogInput = LogInput.replace("\n".encode("utf-8"), os.linesep.encode("utf-8"))
                        self.clFile.write(NewLogInput)
                    else:
                        self.clFile.write(LogInput.decode("utf-8"))
                else:
                    if self.bOpenInBinary:
                        NewLogInput = LogInput.replace("\n", os.linesep)
                        self.clFile.write(NewLogInput.encode("utf-8"))
                    else:
                        self.clFile.write(LogInput)
                return True
            except:
                return False

        return False

    # @Define   Archive the log file
    #
    # @Return   0 : Success, 1 : Error, 2 : Error and FileSetup failed, 3 : FileSetup failed but Copy Success
    #
    # @Note     Archive the file has : FileName Day-Month-Year-??h-??m-??s
    # @Note     Same location has file inside a folder (Log Archive)
    # @Note     File has to be setup in order for this function to work
    #
    def ArchiveFile(self):

        clCounter = Counter()

        if self.bFileOpen:

            #Memorise file settings
            sLogFileName = self.sLogFileName
            sLogFilePosition = self.sLogFilePosition

            bOpenInBinary = self.bOpenInBinary

            #Close file so it is written
            if not self.FileClose():
                return 1

            #Create the archive folder if necessary and copy the file
            try:
                osLogFolder = os.path.dirname(sLogFilePosition + "\\Log Archive\\")

                if not os.path.exists(osLogFolder):
                    os.mkdir(osLogFolder)

                sName, sType = sLogFileName.split(".")
            
                sLogFile = sLogFilePosition + sLogFileName
                sLogFileCopy = sLogFilePosition + "\\Log Archive\\" + sName + " " + clCounter.GetDate(False) + "-" + clCounter.GetTime(False) + "." + sType

                shutil.copy(sLogFile, sLogFileCopy)

            #Redo the Filesetup and return error since we failed the copy
            except:
                if not self.FileSetup(sLogFileName, sLogFilePosition, bOpenInBinary):
                    return 2
                return 1

            #Redo the FileSetup and return error if we fail
            if not self.FileSetup(sLogFileName, sLogFilePosition, bOpenInBinary):
                return 3

        else:
            return 1

        return 0