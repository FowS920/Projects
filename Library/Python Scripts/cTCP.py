from gSettings import *
from cCounter import *
from cLog import *

#TODO : Do not import has *
from threading import *
from socket import *

import struct
import sys
import os

# @Define   RaspberryPI specific defines
#
# @Note     Those have to be "Commented" on windows
# @Note     Those have to be "Uncommented" on RaspberryPI
#
#import fcntl

# @Define   Class used for TCP communication
#
# @Author   Maxime Lagadec
# @Date     1/13/2018
#
class TCP:

    #Class defines
    MAXIMUM_PACKET_SIZE = 4096

    #Variables definition
    sHostIP = "10.0.10.?"   # << Host's IP
    sPeerIP = "10.0.10.?"   # << Peer's IP (Host Only)

    sLogFileName = ""       # << Log file name (Slave Only)
    sLogFilePosition = ""   # << Log file position (Slave Only)
    sSelected_IP = ""       # << IP selected for connection (Slave Only)

    iPort = 4756            # << Port used for commands
    iTimeOut = 5            # << Command port timeout
    iLogPort = 4757         # << Port used for log
    iLogTimeOut = 5         # << Log port timeout

    bTCPHost = False        # << Are we a host
    bConnected = False      # << Are we connected
    bSlaveLogging = False   # << Is the slave logging (Slave Only)
    bLoggingSetup = False   # << Is the log setup done (Slave Only)

    clLog = Log()           # << Log Class (Slave Only)
    clCounter = Counter()   # << Counter Class (Slave Only)

    #clHost_Socket          # << Host Socket (Host Only)
    #clHost_LogSocket       # << Host Log Socket (Host Only)
    #clSlave_Socket         # << Slave Socket (Slave Only)
    #clSlave_LogSocket      # << Slave Log Socket (Slave Only)

    clLocal = local()               # << Local variable for threads ; Value is different for each thread

    #clLocal.clPeer_Socket          # << Peer Socket (Host Only)
    #clLocal.clPeer_LogSocket       # << Peer Log Socket (Host Only)
    #clLocal.clCounter              # << Counter class for the thread (Host only)

    #Slave only variable (Threads and connections)
    #clLoggingThreadStarted = Event()
    #clLoggingThreadStop = Event()
    #clLoggingThreadEnded = Event()

    #Server only variable (Threads and connections)
    #clAcceptationThreadStarted = Event()
    #clAcceptationThreadStop = Event()
    #clAcceptationThreadEnded = Event()

    #clCommunicationThreadStarted = Event()

    # @Define   Initialisation of the class
    #
    # @Param    [in] bIsHost : True if Host, false if Slave
    # @Param    [in, opt.] sHostIP : If Host, IP can be provided
    #
    # @Note     Default host IP is set to 10.0.10.100
    #
    def __init__(self, bIsHost, sHostIP = "10.0.10.100"):

        #Host initialisation
        if bIsHost:
            current_thread().name = "__MAIN_THREAD_"

            self.clAcceptationThreadStarted = Event()
            self.clAcceptationThreadStarted.clear()
            self.clAcceptationThreadStop = Event()
            self.clAcceptationThreadStop.clear()
            self.clAcceptationThreadEnded = Event()
            self.clAcceptationThreadEnded.clear()

            self.clCommunicationThreadStarted = Event()
            self.clCommunicationThreadStarted.clear()

        #Slave initialisation
        else:
            self.clLoggingThreadStarted = Event()
            self.clLoggingThreadStarted.clear()
            self.clLoggingThreadStop = Event()
            self.clLoggingThreadStop.clear()
            self.clLoggingThreadEnded = Event()
            self.clLoggingThreadEnded.clear()

        self.sHostIP = sHostIP
        self.bTCPHost = bIsHost

    # @Define   Destructor of the class
    #
    def __del__(self):
        
        self.Disconnect()

    # @Define   Print to log if possible, normal print otherwise
    #
    # @Note     Host assumes slave is ALWAYS logging
    # @Note     Connection does not work if logging socket does not connect
    #
    def PrintTCP(self, sString):

        if self.bTCPHost:
            if not ((current_thread().name == "__MAIN_THREAD_") or (current_thread().name == "__ACCEPTATION_THREAD_")):
                for sLine in sString.splitlines(True):
                    if not self.SendData(self.clLocal.clPeer_LogSocket, True, "[%s] %s" % (self.Detect_IP(), sLine)):
                        return
                return
        else:
            if self.bSlaveLogging:
                if not self.clLog.Write(sString, False):
                    return
                return

        print(sString)

    # @Define   Setup logging
    #
    # @Param    [in] sLogFileName : Name of the log file
    # @Param    [in] sLogFilePosition : Position of the log file
    #
    # @Note     This must be called in order for log to work
    #
    # @Return   True : Success, False : Error
    #
    def SetupLogging(self, sLogFileName, sLogFilePosition):

        self.bLoggingSetup = False

        #Check if file position is valid
        if not os.path.isdir(sLogFilePosition):
            self.PrintTCP("\nInvalid file position!\n\n")
            return False

        #Check if file name is valid
        #We can't have more then one dot
        if sLogFileName.count(".") > 1:
            self.PrintTCP("\nInvalid file name : more then two dots!\n\n")
            return False
        #If we don't find .log...
        if sLogFileName.find(".log") == -1:
            #If we find a dot
            if not sLogFileName.find(".") == -1:
                self.PrintTCP("\nInvalid file type : must be .log!\n\n")
                return False
            #Add a .log to file name
            else:
                sLogFileName += ".log"

        self.sLogFileName = sLogFileName
        self.sLogFilePosition = sLogFilePosition

        self.bLoggingSetup = True

    # @Define   Start logging prints
    #
    # @Return   True : Success, False : Error
    #
    def StartLogging(self):

        if self.bLoggingSetup == False:
            self.PrintTCP("\nCouldn't start log : setup has not been done!\n\n")
            return False

        if self.bSlaveLogging == True:
            self.PrintTCP("\nCouldn't start log : it is already started!\n\n")
            return False

        #Setup Log File
        #Log file absolutly has to be opened in binary for this class to work
        if not self.clLog.FileSetup(self.sLogFileName, self.sLogFilePosition, True):
            self.PrintTCP("\nCouldn't start log : file setup did not succeed!\n\n")
            return False

        #Set logging to true
        self.bSlaveLogging = True

        self.PrintTCP("\nStarting Log >> %s ; %s\n\n" % (self.clCounter.GetDate(False), self.clCounter.GetTime(False)))

        return True

    # @Define   Stop logging prints
    #
    # @Return   True : Success, False : Error
    #
    # @Note     This also archive the log
    #
    def StopLogging(self):

        if self.bSlaveLogging == False:
            self.PrintTCP("\nCouldn't stop log : it is not started yet!\n\n")
            return False

        self.PrintTCP("\nEnding Log >> %s ; %s\n\n" % (self.clCounter.GetDate(False), self.clCounter.GetTime(False)))

        #Set logging to false
        self.bSlaveLogging = False

        #Archive Log File
        if self.clLog.ArchiveFile():
            self.PrintTCP("\nCouldn't archive log file!\n\n")
            return False

        #Close Log File
        if not self.clLog.FileClose():
            self.PrintTCP("\nCouldn't close log file!\n\n")
            return False

        return True

    # @Define   Detect available network IP
    #
    # @Return   Return string with found IP
    #
    # @Note     Only works on the raspberry PI
    #
    def Detect_IP(self):

        clTempSocket = socket(AF_INET, SOCK_DGRAM)

        return inet_ntoa(fcntl.ioctl(clTempSocket.fileno(), 0x8915, struct.pack("256s", b"eth0"))[20:24])

    # @Define   Connect to the HOST/SLAVE
    #
    # @Param    [in] sIP : IP used for connect (Slave side)
    #
    # @Return   True : Success, False : Error
    #
    def Connect(self, sIP = ""):

        if self.bConnected:
            self.PrintTCP("\nWe are already connected!\n\n")

        else:

            bSocketCreated = False
            bLogSocketCreated = False

            if self.bTCPHost:

                if self.Detect_IP() != self.sHostIP:
                    self.PrintTCP("\nHost IP is not configured properly!\n\n")
                    return False

                try:
                    #Create Host Socket
                    self.clHost_Socket = socket(AF_INET, SOCK_STREAM, 0, None)
                    bSocketCreated = True
                    self.clHost_Socket.settimeout(self.iTimeOut)
                    self.clHost_Socket.bind((self.sHostIP, self.iPort))
                    self.clHost_Socket.listen(5)

                    #Create Host Log Socket
                    self.clHost_LogSocket = socket(AF_INET, SOCK_STREAM, 0, None)
                    bLogSocketCreated = True
                    self.clHost_LogSocket.settimeout(self.iLogTimeOut)
                    self.clHost_LogSocket.bind((self.sHostIP, self.iLogPort))
                    self.clHost_LogSocket.listen(5)

                    #Start Accepting Connection Attempts
                    if not self.StartAcceptationThread():
                        self.PrintTCP("\nError while trying to start acceptation thread!\n\n")
                        raise Exception("Could not start acceptation thread...")

                    self.bConnected = True
                except:

                    if bSocketCreated == True:
                        self.clHost_Socket.close()
                    if bLogSocketCreated == True:
                        self.clHost_LogSocket.close()

                    self.bConnected = False
                    return False

            else:

                try:
                    #Create Slave Socket
                    self.clSlave_Socket  = socket(AF_INET, SOCK_STREAM, 0, None)
                    bSocketCreated = True
                    self.clSlave_Socket.settimeout(self.iTimeOut)
                    self.clSlave_Socket.connect((sIP, self.iPort))

                    #Create Slave Log Socket
                    self.clSlave_LogSocket  = socket(AF_INET, SOCK_STREAM, 0, None)
                    bLogSocketCreated = True
                    self.clSlave_LogSocket.settimeout(self.iLogTimeOut)
                    self.clSlave_LogSocket.connect((sIP, self.iLogPort))

                    if not self.StartLoggingThread():
                        self.PrintTCP("\nError while trying to start logging thread!\n\n")
                        raise Exception("Could not start logging thread...")

                    self.bConnected = True
                except:
                    
                    if bSocketCreated == True:
                        self.clSlave_Socket.close()
                    if bLogSocketCreated == True:
                        self.clSlave_LogSocket.close()

                    self.bConnected = False
                    return False

        return True

    # @Define   Disconnect from the HOST/SLAVE
    #
    # @Return   True : Success, False : Error
    #
    def Disconnect(self):
        
        if self.bConnected:

            try:
                if self.bTCPHost:
                    if not self.StopAcceptationThread():
                        self.PrintTCP("\nError while trying to stop acceptation thread!\n\n")
                        raise Exception("Could not stop acceptation thread...")

                    try:
                        self.clHost_Socket.close()
                    except:
                        pass
                    try:
                        self.clHost_LogSocket.close()
                    except:
                        pass

                    self.bConnected = False

                else:
                    if not self.StopLoggingThread():
                        self.PrintTCP("\nError while trying to stop logging thread!\n\n")
                        raise Exception("Could not stop logging thread...")

                    try:
                        self.clSlave_Socket.shutdown(SHUT_RDWR)
                    except:
                        pass
                    try:
                        self.clSlave_Socket.close()
                    except:
                        pass
                    try:
                        self.clSlave_LogSocket.shutdown(SHUT_RDWR)
                    except:
                        pass
                    try:
                        self.clSlave_LogSocket.close()
                    except:
                        pass

                    self.bConnected = False
            except:
                return False

        else:
            self.PrintTCP("\nWe are already disconnected!\n\n")

        return True

    # @Define   Accept incoming connection on HOST
    #
    # @Return   True : Success, False : Error
    #
    # @Note     For multiple connections use with
    # @Note     StartCommunicationThread for every accept
    #
    def Accept(self):

        if self.bConnected:

            if self.bTCPHost:

                try:
                    self.clPeer_Socket, self.sPeerIP = self.clHost_Socket.accept()
                    self.clPeer_Socket.settimeout(self.iTimeOut)
                    self.clPeer_LogSocket, self.sPeerIP = self.clHost_LogSocket.accept()
                    self.clPeer_LogSocket.settimeout(self.iLogTimeOut)
                except:
                    return False

                return True

            else:
                self.PrintTCP("\nOnly host can accept connections!\n\n")
                return False

        return False

    # @Define   Start acceptation thread
    #
    # @Return   True : Success, False : Error
    #
    def StartAcceptationThread(self):

        self.clAcceptationThreadStarted.clear()
        self.clAcceptationThreadStop.clear()
        self.clAcceptationThreadEnded.clear()

        t = Thread(target = self.AcceptationThread)
        t.start()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 3) and (not self.clAcceptationThreadStarted.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clAcceptationThreadStarted.is_set():
            return False

        return True

    # @Define   Start logging thread
    #
    # @Return   True : Success, False : Error
    #
    def StartLoggingThread(self):

        self.clLoggingThreadStarted.clear()
        self.clLoggingThreadStop.clear()
        self.clLoggingThreadEnded.clear()

        t = Thread(target = self.LoggingThread)
        t.start()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 3) and (not self.clLoggingThreadStarted.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clLoggingThreadStarted.is_set():
            return False

        return True

    # @Define   Start communication thread
    #
    # @Return   True : Success, False : Error
    #
    def StartCommunicationThread(self):

        self.clCommunicationThreadStarted.clear()

        t = Thread(target = self.CommunicationThread)
        t.start()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 3) and (not self.clCommunicationThreadStarted.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clCommunicationThreadStarted.is_set():
            return False

        return True

    # @Define   Stop acceptation thread
    #
    # @Return   True : Success, False : Error
    #
    def StopAcceptationThread(self):

        self.clAcceptationThreadStop.set()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 120) and (not self.clAcceptationThreadEnded.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clAcceptationThreadEnded.is_set():
            return False

        return True

    # @Define   Stop logging thread
    #
    # @Return   True : Success, False : Error
    #
    def StopLoggingThread(self):

        self.clLoggingThreadStop.set()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 3) and (not self.clLoggingThreadEnded.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clLoggingThreadEnded.is_set():
            return False
        
        return True

    # @Define   Receive Data from HOST/SLAVE
    #
    # @Param    [in] clSocket : Socket to receive data from
    # @Param    [in] bString : True to receive a string, false to receive an integer
    #
    # @Return   Data received (string if bString True, integer if bString False)
    #
    # @Note     Integer is NULL if receive did not work
    # @Note     String is EMPTY if receive did not work
    #
    def ReceiveData(self, clSocket, bString):
        
        #Reset Data
        if bString:
            Data = ""
        else:
            Data = 0

        #Receive Data
        try:
            byData = clSocket.recv(self.MAXIMUM_PACKET_SIZE)
        except:
            return Data

        #Convert into string/integer
        #Execept if we didn't receive anything
        try:
            if bString:
                Data = byData.decode("utf-8")
                Data.replace("\r\n", "\n")
            else:
                Data = struct.unpack("i", byData)[0]
        except:
            return Data
        return Data

    # @Define   Send Data to HOST/SLAVE
    #
    # @Param    [in] clSocket : Socket to send data from
    # @Param    [in] bString : True to send a string, false to send an integer
    # @Param    [in] Data : Data to be sent
    #
    # @Return   True : Success, False : Error
    #
    def SendData(self, clSocket, bString, Data):

        #Check size of data
        if sys.getsizeof(Data) > self.MAXIMUM_PACKET_SIZE:
            return False

        #Send data has bytes
        try:
            if bString:
                Data.replace("\n", "\r\n")
                clSocket.send(Data.encode("utf-8"))
                return True
            else:
                clSocket.send(struct.pack("i", Data))
                return True
        except:
            return False

    # @Define   Acception thread definition
    #
    # @Note     This thread is only applicable
    # @Note     Server Side (accept peer connection)
    #
    def AcceptationThread(self):

        current_thread().name = "__ACCEPTATION_THREAD_"

        self.clAcceptationThreadStarted.set()

        while not self.clAcceptationThreadStop.is_set():

            if self.Accept():
                
                #Create thread here
                self.PrintTCP("Connection accepted! Starting thread... ")
                if self.StartCommunicationThread() :
                    self.PrintTCP("Done!\n\n")
                else:
                    self.PrintTCP("Error!\n\n")

        self.clAcceptationThreadEnded.set()

        return

    # @Define   Logging thread definition
    #
    # @Note     This thread is only applicable
    # @Note     Slave Side (only one logging thread)
    #
    def LoggingThread(self):

        self.clLoggingThreadStarted.set()

        while not self.clLoggingThreadStop.is_set():

            byData = "".encode("utf-8")

            try:
                byData = self.clSlave_LogSocket.recv(self.MAXIMUM_PACKET_SIZE)
            except:
                continue

            if self.bSlaveLogging:
                self.clLog.Write(byData, True)

        self.clLoggingThreadEnded.set()

    # @Define   Communication thread definition
    #
    # @Note     This thread is only applicable
    # @Note     Server Side (one per peer connection)
    #
    def CommunicationThread(self):

        #Initialize thread variables
        self.clLocal.clPeer_Socket = self.clPeer_Socket
        self.clLocal.clPeer_LogSocket = self.clPeer_LogSocket
        self.clLocal.sPeerIP = self.sPeerIP
        self.clLocal.clCounter = Counter()
        
        #Set thread name
        current_thread().name = "__COMMUNICATION_THREAD_"

        #Thread is started
        self.clCommunicationThreadStarted.set()

        #Receive action
        iData = self.ReceiveData(self.clLocal.clPeer_Socket, False)

        if not iData == 0:
            self.PrintTCP("\nAction #%d Request Received... Executing...\n\n" % (iData))

        #Project Specific Actions
        if iData >= 1000:
            try:
                for ACTIONS in ACTIONS_LIST:
                    if ACTIONS[1] == iData:
                        if not getattr(sys.modules[__name__], "%s" % (ACTIONS[0]))(self.clTCP):
                            self.PrintTCP("\nAction #%d Failed!\n\n" % (iData))
            except:
                self.PrintTCP("\nCould not find action #d!\n\n" % (iData))

        #Actions
        elif iData > 0:
            if not self.Actions(iData):
                self.PrintTCP("\nAction #%d Failed!\n\n" % (iData))

        #Did not receive command
        else:
            self.PrintTCP("\nThread started but no input were sent!\n\n")

        #Close connections
        try:
            self.clLocal.clPeer_Socket.close()
        except:
            pass
        try:
            self.clLocal.clPeer_LogSocket.close()
        except:
            pass

        return

    # @Define   Switch case for all possible actions
    #
    # @Param    [in] iData : Action to be executed
    # @Param    [in, opt.] sOptionA : First option
    # @Param    [in, opt.] sOptionB : Second option
    #
    # @Return   True : Success, False : Error
    #
    # @Note     Actions are avaible to all projects, make them generic
    #
    def Actions(self, iData, sOptionA = "", sOptionB = ""):

        #Connect to host if slave
        if not self.bTCPHost:
            if not self.Connect(self.sSelected_IP):
                self.PrintTCP("\nCould not connect properly!\n\n")
                return False

        if iData < 0 or iData > 2:
            return False

        switch_case = {
            1: self.SendFile,
            2: self.ReceiveFile
        }

        bSuccess =  switch_case[iData](sOptionA, sOptionB)

        #Disonnect from host if slave
        if not self.bTCPHost:
            if not self.Disconnect():
                self.PrintTCP("\nCould not disconnect properly!\n\n")
                return False

        return bSuccess

    # @Define   Send a file to target destination from target location
    #
    # @Param    [in] sLocation : Location of the file
    # @Param    [in] sDestination : Destination of the file
    #
    # @Return   True : Success, False : Error   
    #
    # @Note     SendFile is hardcoded in pair with ReceiveFile
    #
    def SendFile(self, sLocation, sDestination):

        #Data variables
        sData = ""
        iData = 0

        #Check if file location is valid for Slave
        if not self.bTCPHost:
            if not os.path.isfile(sLocation):
                self.PrintTCP("Bad file location on local computer!\n")
                return False

        #Slave initialisation
        if not self.bTCPHost:
            clSocket = self.clSlave_Socket
            self.SendData(clSocket, False, 2)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

        #Server initialisation
        else:
            clSocket = self.clLocal.clPeer_Socket
            self.SendData(clSocket, True, "ACK")

        #Slave action
        if not self.bTCPHost:

            #Send destination
            self.SendData(clSocket, True, sDestination)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                self.PrintTCP("Bad file location on remote computer!\n")
                return False

        #Server action
        else:
            #Receive location
            sLocation = self.ReceiveData(clSocket, True)
            if sLocation == "":
                self.SendData(clSocket, True, "NACK")
                return False

        #Open file in read binary
        try:
            clFile = open(sLocation, "rb")
            clFile.seek(0, 0)
        except:
            if self.bTCPHost:
                self.SendData(clSocket, True, "NACK")
            return False

        if self.bTCPHost:
            self.PrintTCP("Sending Files.\n\n")
            self.SendData(clSocket, True, "ACK")

        #Send file size
        self.SendData(clSocket, False, os.stat(sLocation).st_size)
        sData = self.ReceiveData(clSocket, True)
        if not sData == "ACK":
            clFile.close()
            return False

        #Send file
        clSocket.sendfile(clFile)
        sData = self.ReceiveData(clSocket, True)
        if not sData == "ACK":
            clFile.close()
            return False

        if self.bTCPHost:
            self.PrintTCP("File sent.\n\n")

        clFile.close()
        return True

    # @Define   Receive a file to target destination
    #
    # @Param    [in] sLocation : Location of the file
    # @Param    [in] sDestination : Destination of the file
    #
    # @Return   True : Success, False : Error
    #
    # @Note     SendFile is hardcoded in pair with SendFile
    #
    def ReceiveFile(self, sLocation, sDestination):

        #Data variables
        sData = ""
        iData = 0

        #Specific variables
        iFileSize = 0
        iBytesReceived = 0
        byReceivedBytes = 0x0

        #Check if file destination is valid for Slave
        if not self.bTCPHost:
            try:
                if not os.path.isdir(sDestination[:(sDestination.rfind("\\") + 1)]):
                    self.PrintTCP("Bad file location on local computer!\n")
                    return False
            except:
                return False

        #Slave initialisation
        if not self.bTCPHost:
            clSocket = self.clSlave_Socket
            self.SendData(clSocket, False, 1)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

        #Server initialisation
        else:
            clSocket = self.clLocal.clPeer_Socket
            self.SendData(clSocket, True, "ACK")

        #Slave action
        if not self.bTCPHost:

            #Send location
            self.SendData(clSocket, True, sLocation)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                self.PrintTCP("Bad file location on remote computer!\n")
                return False

        #Server action
        else:
            #Receive destination
            sDestination = self.ReceiveData(clSocket, True)
            if sDestination == "":
                self.SendData(clSocket, True, "NACK")
                return False

        #Open file in write binary (+ creates it if does not exist)
        try:
            clFile = open(sDestination, "ab+")
            clFile.seek(0, 0)
        except:
            if self.bTCPHost:
                self.SendData(clSocket, True, "NACK")
            return False

        if self.bTCPHost:
            self.PrintTCP("Receiving Files.\n\n")
            self.SendData(clSocket, True, "ACK")

        #Receive file size
        iFileSize = self.ReceiveData(clSocket, False)

        if not iFileSize == 0:
            self.SendData(clSocket, True, "ACK")
        else:
            self.SendData(clSocket, True, "NACK")
            clFile.close()
            return False

        #Receive file
        while iFileSize > 0:
            byReceivedBytes = clSocket.recv(self.MAXIMUM_PACKET_SIZE)
            iBytesReceived = len(byReceivedBytes)

            clFile.write(byReceivedBytes)

            iFileSize = iFileSize - iBytesReceived

        clFile.close()

        if self.bTCPHost:
            self.PrintTCP("File received.\n\n")

        self.SendData(clSocket, True, "ACK")

        return True