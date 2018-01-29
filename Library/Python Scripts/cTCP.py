from threading import *
from socket import *
from cCounter import *

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
    sHostIP = "10.0.10.100"
    sPeerIP = "10.0.10.?"

    iPort = 4756
    iTimeOut = 5

    bTCPHost = False
    bConnected = False

    #clHost_Socket
    #clSlave_Socket
    #clPeer_Socket

    #Server only variable (number of clients connected)
    iConnections = 0

    clThreadStarted = Event()
    clThreadStop = Event()

    # @Define   Initialisation of the class
    #
    def __init__(self, bIsHost):

        self.clThreadStarted.clear()
        self.clThreadStop.clear()
        self.bTCPHost = bIsHost

    # @Define   Destructor of the class
    def __del__(self):
        
        self.Disconnect()

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
            print("We are already connected!\n")

        else:

            if self.bTCPHost:

                if self.Detect_IP() != self.sHostIP:
                    print("Host IP is not configured properly!\n")
                    return False

                try:
                    self.clHost_Socket = socket(AF_INET, SOCK_STREAM, 0, None)
                    bSocketCreated = True
                    self.clHost_Socket.settimeout(self.iTimeOut)
                    self.clHost_Socket.bind((self.sHostIP, self.iPort))
                    self.clHost_Socket.listen(5)

                    if not self.StartAcceptationThread():
                        print("Error while trying to start acceptation thread!")
                        raise Exception("Could not start acceptation thread...")

                    self.bConnected = True
                except:

                    if bSocketCreated == True:
                        self.clHost_Socket.close()

                    self.bConnected = False
                    return False

            else:

                try:
                    self.clSlave_Socket  = socket(AF_INET, SOCK_STREAM, 0, None)
                    bSocketCreated = True
                    self.clSlave_Socket.settimeout(self.iTimeOut)
                    self.clSlave_Socket.connect((sIP, self.iPort))
                    self.bConnected = True
                except:
                    
                    if bSocketCreated == True:
                        self.clSlave_Socket.close()

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
                        print("Error while trying to stop threads!")

                    self.clHost_Socket.close()

                    self.bConnected = False

                else:
                    #Kill thread associated
                    self.SendData(self.clSlave_Socket, False, 404)

                    self.clSlave_Socket.shutdown(SHUT_RDWR)
                    self.clSlave_Socket.close()

                    self.bConnected = False
            except:
                return False

        else:
            print("We are already disconnected!\n")

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
                except:
                    return False

                return True

            else:
                print("Only host can accept connections!\n")
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
                print("Connection accepted! Starting thread...")
                self.StartCommunicationThread()
                print("Number of threads : {0}\n".format(self.iConnections))

        return

    # @Define   Communication thread definition
    #
    # @Note     This thread is only applicable
    # @Note     Server Side (one per peer connection)
    #
    def CommunicationThread(self):

        clPeer_Socket = self.clPeer_Socket
        sPeerIP = self.sPeerIP

        sData = ""
        iData = 0

        print("Thread started!")
        self.clThreadStarted.set()

        #Main loop for thread
        while not self.clThreadStop.is_set():

            iData = self.ReceiveData(clPeer_Socket, False)

            #Disconnect
            if iData == 404:

                break

            #Actions
            if iData > 0:
                #If fail clear the socket stream
                self.Actions(clPeer_Socket, iData)

        #Thread forced to shutdown by host
        try:
            clPeer_Socket.shutdown(SHUT_RDWR)
        except:
            print("Connection was already closed!")
        try:
            clPeer_Socket.close()
        except:
            print("Could not close correctly!")

        self.iConnections = self.iConnections - 1
        print("Thread stopped!")
        print("Number of threads : {0}\n".format(self.iConnections))

        return

    # @Define   Switch case for all possible actions
    #
    # @Param    [in] clSocket : Socket on which action applies
    # @Param    [in] iData : Action to be executed
    # @Param    [in, opt.] sOptionA : First option
    # @Param    [in, opt.] sOptionB : Second option
    #
    # @Return   True : Success, False : Error
    #
    # @Note     clSocket is only required for hosts, use NULL (0) for slaves
    # @Note     Actions are avaible to all projects, make them generic
    #
    def Actions(self, clSocket, iData, sOptionA = "", sOptionB = ""):
        
        switch_case = {
            1: self.SendFile,
            2: self.ReceiveFile,
        }

        #If function fails, clear the socket stream
        #When function does not fail, it means no data is present in the stream
        if not switch_case[iData](clSocket, sOptionA, sOptionB):
            try:
                #Host peer socket
                if self.bTCPHost:
                    byData = clSocket.recv(self.MAXIMUM_PACKET_SIZE)
                    while(len(byData)):
                        byData = clSocket.recv(self.MAXIMUM_PACKET_SIZE)
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
    # @Param    [in] clSocket : Socket to receive file from
    # @Param    [in] sLocation : Location of the file
    # @Param    [in] sDestination : Destination of the file
    #
    # @Return   True : Success, False : Error   
    #
    # @Note     clSocket is only required for hosts, use NULL (0) for slaves
    # @Note     SendFile is hardcoded in pair with ReceiveFile
    #
    def SendFile(self, clSocket, sLocation, sDestination):

        #Data variables
        sData = ""
        iData = 0

        print("Sending Files")

        #Client initialisation
        if not self.bTCPHost:
            clSocket = self.clSlave_Socket
            self.SendData(clSocket, False, 2)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

        #Server response
        else:
            self.SendData(clSocket, True, "ACK")

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
    # @Param    [in] clSocket : Socket to receive file from
    # @Param    [in] sLocation : Location of the file
    # @Param    [in] sDestination : Destination of the file
    #
    # @Return   True : Success, False : Error
    #
    # @Note     clSocket is only required for hosts, use NULL (0) for slaves
    # @Note     SendFile is hardcoded in pair with SendFile
    #
    def ReceiveFile(self, clSocket, sLocation, sDestination):

        #Data variables
        sData = ""
        iData = 0

        #Specific variables
        iFileSize = 0
        iBytesReceived = 0
        byReceivedBytes = 0x0

        print("Receiving Files")

        #Client initialisation
        if not self.bTCPHost:
            clSocket = self.clSlave_Socket
            self.SendData(clSocket, False, 1)
            sData = self.ReceiveData(clSocket, True)
            if not sData == "ACK":
                return False

        #Server response
        else:
            self.SendData(clSocket, True, "ACK")

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