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
    sHostIP = "10.0.10.?"   # << Host's IP (Slave Only)
    sPeerIP = "10.0.10.?"   # << Peer's IP (Host Only)

    iPort = 4756            # << Port used for commands
    iTimeOut = 5            # << Command port timeout

    iLogPort = 4757         # << Port used for log
    iLogTimeOut = 5         # << Log port timeout

    bTCPHost = False        # << Are we a host
    bConnected = False      # << Are we connected
    bSlaveLogging = False   # << Is the slave logging

    clLog = Log()           # << Log Class (Slave Only)

    #clHost_Socket          # << Host Socket (Host Only)
    #clHost_LogSocket       # << Host Log Socket (Host Only)
    #clSlave_Socket         # << Slave Socket (Slave Only)
    #clSlave_LogSocket      # << Slave Log Socket (Slave Only)

    clLocal = local()               # << Local variable for threads ; Value is different for each thread

    #clLocal.clPeer_Socket          # << Peer Socket (Host Only)
    #clLocal.clPeer_LogSocket       # << Peer Log Socket (Host Only)
    #clLocal.bLogging               # << Are we logging prints (Host only)
    #clLocal.clCounter              # << Counter class for the thread (Host only)

    #Slave only variable (Threads and connections)
    clLoggingThreadStarted = Event()
    clLoggingThreadStop = Event()
    clLoggingThreadEnded = Event()

    #Server only variable (Threads and connections)
    iConnections = 0

    clThreadStarted = Event()
    clThreadStop = Event()

    # @Define   Initialisation of the class
    #
    # @Param    [in] bIsHost : True if Host, false if Slave
    # @Param    [in, opt.] sHostIP : If Host, IP can be provided
    #
    # @Note     Default host IP is set to 10.0.10.100
    #
    def __init__(self, bIsHost, sHostIP = "10.0.10.100"):

        self.clThreadStarted.clear()
        self.clThreadStop.clear()
        self.bTCPHost = bIsHost
        self.sHostIP = sHostIP

    # @Define   Destructor of the class
    def __del__(self):
        
        self.Disconnect()

    # @Define   Print to log if possible, normal print otherwise
    #
    def PrintTCP(self, sString):

        if self.bTCPHost:
            if current_thread().name == "THREADING":
                if self.clLocal.bLogging:
                    if self.SendData(self.clLocal.clPeer_LogSocket, True, "[%s] %s" % (self.Detect_IP(), sString)):
                        return
        else:
            if self.bSlaveLogging:
                if self.clLog.Write(sString, False):
                    return

        print(sString)

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
    # @Param    [in] sIP : IP used for connect (client side)
    #
    # @Return   True : Success, False : Error
    #
    def Connect(self, sIP = ""):

        if self.bConnected:
            self.PrintTCP("We are already connected!\n")

        else:

            if self.bTCPHost:

                if self.Detect_IP() != self.sHostIP:
                    self.PrintTCP("Host IP is not configured properly!\n")
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
                        self.PrintTCP("Error while trying to start acceptation thread!")
                        raise Exception("Could not start acceptation thread...")

                    self.bConnected = True
                except:

                    if bSocketCreated == True:
                        self.clHost_Socket.close()
                    if bLogSocketCreated == True:
                        self.clHost_LoggingSocket.close()

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
                    if not self.StopThreads():
                        self.PrintTCP("Error while trying to stop threads!")

                    self.clHost_Socket.close()
                    self.clHost_LogSocket.close()

                    self.bConnected = False

                else:
                    #Kill thread associated
                    self.SendData(self.clSlave_Socket, False, 404)

                    self.clSlave_Socket.shutdown(SHUT_RDWR)
                    self.clSlave_Socket.close()
                    self.clSlave_LogSocket.shutdown(SHUT_RDWR)
                    self.clSlave_Socket.close()

                    self.bConnected = False
            except:
                return False

        else:
            self.PrintTCP("We are already disconnected!\n")

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
                self.PrintTCP("Only host can accept connections!\n")
                return False

        return False

    # @Define   Start acceptation thread
    #
    # @Return   True : Success, False : Error
    #
    def StartAcceptationThread(self):

        self.clThreadStarted.clear()
        self.clThreadStop.clear()

        t = Thread(target = self.AcceptationThread)
        t.start()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 3) and (not self.clThreadStarted.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clThreadStarted.is_set():
            return False

        return True

    # @Define   Start logging thread
    #
    # @Return   True : Success, False : Error
    #
    def StartLoggingThread(self, clSocket):

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

        self.clThreadStarted.clear()
        self.clThreadStop.clear()

        t = Thread(target = self.CommunicationThread)
        t.start()

        clCounter = Counter()
        clCounter.StartCounter()

        while ((clCounter.GetCounterValue() < 3) and (not self.clThreadStarted.is_set())):
            pass

        clCounter.ResetCounter()

        if not self.clThreadStarted.is_set():
            return False

        self.iConnections = self.iConnections + 1

        return True

    # @Define   Stop communication/acceptation thread(s)
    #
    # @Return   True : Success, False : Error
    #
    def StopThreads(self):

        if self.iConnections == 0:
            return True

        self.clThreadStop.set()

        clCounter = Counter()
        clCounter.StartCounter()

        #Give 2 minutes for threads to stop
        while ((clCounter.GetCounterValue() < 120) and (self.iConnections != 0)):
            pass

        clCounter.ResetCounter()

        if self.iConnections != 0:
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

        self.clThreadStarted.set()

        while not self.clThreadStop.is_set():

            if self.Accept():
                
                #Create thread here
                self.PrintTCP("Connection accepted! Starting thread...")
                if self.StartCommunicationThread() :
                    self.PrintTCP("Number of threads : {0}\n".format(self.iConnections))

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

            self.clLog.Write(byData, True)

        self.clLoggingThreadEnded.set()

    # @Define   Communication thread definition
    #
    # @Note     This thread is only applicable
    # @Note     Server Side (one per peer connection)
    #
    def CommunicationThread(self):

        #Initialize thread variables
        current_thread().name = "THREADING"

        self.clLocal.clPeer_Socket = self.clPeer_Socket
        self.clLocal.clPeer_LogSocket = self.clPeer_LogSocket
        self.clLocal.sPeerIP = self.sPeerIP
        self.clLocal.bLogging = False
        self.clLocal.clCounter = Counter()

        sData = ""
        iData = 0

        self.PrintTCP("Thread started!")
        self.clThreadStarted.set()

        #Main loop for thread
        while not self.clThreadStop.is_set():

            iData = self.ReceiveData(self.clLocal.clPeer_Socket, False)

            #Disconnect
            if iData == 404:
                break

            #Actions
            elif iData > 0:
                self.PrintTCP("Action #%d Request Received... Executing... " % (iData))
                #If fail clear the socket stream
                self.Actions(iData)

        #Thread forced to shutdown by host
        try:
            self.clLocal.clPeer_Socket.shutdown(SHUT_RDWR)
        except:
            self.PrintTCP("Connection was already closed!")
        try:
            self.clLocal.clPeer_Socket.close()
        except:
            self.PrintTCP("Could not close correctly!")

        self.iConnections = self.iConnections - 1
        self.PrintTCP("Thread stopped!")
        self.PrintTCP("Number of threads : {0}\n".format(self.iConnections))

        return

    # @Define   Switch case for all possible actions
    #
    # @Param    [in] iData : Action to be executed
    # @Param    [in, opt.] sOptionA : First option
    # @Param    [in, opt.] sOptionB : Second option
    #
    # @Return   True : Success, False : Error
    #
    # @Note     clSocket is only required for hosts, use NULL (0) for slaves
    # @Note     Actions are avaible to all projects, make them generic
    #
    def Actions(self, iData, sOptionA = "", sOptionB = ""):
        
        switch_case = {
            1: self.SendFile,
            2: self.ReceiveFile,
            3: self.StartLogging,
            4: self.StopLogging
        }

        #If function fails, clear the socket stream
        #When function does not fail, it means no data is present in the stream
        if not switch_case[iData](sOptionA, sOptionB):
            try:
                #Host peer socket
                if self.bTCPHost:
                    byData = self.clLocal.clPeer_Socket.recv(self.MAXIMUM_PACKET_SIZE)
                    while(len(byData)):
                        byData = self.clLocal.clPeer_Socket.recv(self.MAXIMUM_PACKET_SIZE)
                #Slave socket
                else:
                    byData = self.clSlave_Socket.recv(self.MAXIMUM_PACKET_SIZE)
                    while(len(byData)):
                        byData = self.clSlave_Socket.recv(self.MAXIMUM_PACKET_SIZE)
            #Catch timeout errors from socket
            except OSError:
                return False

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

        #Client initialisation
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

            self.PrintTCP("Sending Files.\n\n")

        #Client action
        if not self.bTCPHost:

            #Send destination
            self.SendData(clSocket, True, sDestination)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
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

        #Client initialisation
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

            self.PrintTCP("Receiving Files.\n\n")

        #Client action
        if not self.bTCPHost:

            #Send location
            self.SendData(clSocket, True, sLocation)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
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
        self.SendData(clSocket, True, "ACK")

        return True

    # @Define   Start logging prints
    #
    # @Param    [in] sLogFileName : Name of the log file
    # @Param    [in] sLogFilePosition : Position of the log file
    #
    # @Return   True : Success, False : Error
    #
    def StartLogging(self, sLogFileName, sLogFilePosition):

        #Data variables
        sData = ""
        iData = 0

        #Client initialisation
        if not self.bTCPHost:
            clSocket = self.clSlave_Socket
            self.SendData(clSocket, False, 3)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

        #Server initialisation
        else:
            clSocket = self.clLocal.clPeer_Socket
            self.SendData(clSocket, True, "ACK")

        #Client action
        if not self.bTCPHost:

            #Start Log File
            if not self.clLog.FileSetup(sLogFileName, sLogFilePosition, True):
                self.SendData(clSocket, True, "NACK")

            #Start LoggingThread
            if not self.StartLoggingThread(clSocket):
                self.SendData(clSocket, True, "NACK")
                self.clLog.FileClose()

            #Set logging to true
            self.bSlaveLogging = True

            #Let host know we succeeded
            self.SendData(clSocket, True, "ACK")

        #Server action
        else:

            #Make sure slave initiated correctly
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

            self.clLocal.bLogging = True

            self.PrintTCP("\nStarting Log >> %s ; %s\n\n" % (self.clLocal.clCounter.GetDate(False), self.clLocal.clCounter.GetTime(False)))

            #Nothing else to do, the variable is set in CommunicationThread

        return True

    # @Define   Stop logging prints
    #
    # @Param    [in] sNotUsed_A : Not used
    # @Param    [in] sNotUsed_B : Not used
    #
    # @Return   True : Success, False : Error
    #
    def StopLogging(self, sNotUsed_A, sNotUsed_B):

        #Data variables
        sData = ""
        iData = 0

        #Client initialisation
        if not self.bTCPHost:
            clSocket = self.clSlave_Socket
            self.SendData(clSocket, False, 4)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

        #Server initialisation
        else:
            clSocket = self.clLocal.clPeer_Socket
            self.SendData(clSocket, True, "ACK")

            self.PrintTCP("\nEnding Log >> %s ; %s\n\n" % (self.clLocal.clCounter.GetDate(False), self.clLocal.clCounter.GetTime(False)))

        #Client action
        if not self.bTCPHost:

            #Stop LoggingThread
            if not self.StopLoggingThread():
                self.SendData(clSocket, True, "NACK")
                return False

            #Archive Log File
            if self.clLog.ArchiveFile():
                self.SendData(clSocket, True, "NACK")
                return False

            #Close Log File
            if not self.clLog.FileClose():
                self.SendData(clSocket, True, "NACK")
                return False

            #Set logging to false
            self.bSlaveLogging = False

            #Let host know we succeeded
            self.SendData(clSocket, True, "ACK")

        #Server action
        else:

            #Make sure slave initiated correctly
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

            self.clLocal.bLogging = False

            #Nothing else to do, variable unset in CommunicationThread

        return True