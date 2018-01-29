from time import *
from ASCII import *

# @Define   RaspberryPI specific defines
#
# @Note     Those have to be "Commented" on windows
# @Note     Those have to be "Uncommented" on RaspberryPI
#
#import Rpi.GPIO as GPIO

# @Define   Class used to control LCD
#
# @Author   Maxime Lagadec
# @Date     7/12/2017
#
# @Note     This class only works on the Raspberry PI
# @Note     LCD is the NHD-C12864A1Z-FSRGB-FBW-HT1
#
class LCD:

    #Initialisation of the class
    def __init__(self):

        self.GPIO_setup()
        self.Initialisation()

    def __del__(self):

        self.Clear()
        self.Close()

    #Initial GPIO setup
    def GPIO_setup(self):
        
        #GPIO initial setup
        GPIO.setmode(GPIO.BCM)
        #A0
        GPIO.setup(4, GPIO.OUT)
        GPIO.output(4, True)
        #Reset
        GPIO.setup(17, GPIO.OUT)
        GPIO.output(17, True)
        #CS
        GPIO.setup(27, GPIO.OUT)
        GPIO.output(27, True)
        #SCL
        GPIO.setup(23, GPIO.OUT)
        GPIO.output(23, True)
        #SI
        GPIO.setup(24, GPIO.OUT)
        GPIO.output(24, True)
        #COLOR CONTROL : Blue
        GPIO.setup(26, GPIO.OUT)
        GPIO.output(26, True)
        #COLOR CONTROL : Green
        GPIO.setup(19, GPIO.OUT)
        GPIO.output(19, True)
        #COLOR CONTROL : Red
        GPIO.setup(13, GPIO.OUT)
        GPIO.output(13, True)
        #I2C initial setup

    #Call first to open up the LCD properly
    #According to newhaven display
    def Initialisation(self):
        
        self.Reset()
        #A0 = 1010 0000 (F8)
        self.Command(8, 0xA0)
        #AE = 1010 1110 (F9)
        self.Command(9, 0xAE)
        #C0 = 1100 0000 (F15)
        self.Command(15, 0xC0)
        #A2 = 1010 0010 (F11)
        self.Command(11, 0xA2)
        #2F = 0010 1111 (F16)
        self.Command(16, 0x2F)
        #26 = 0010 0110 (F17)
        self.Command(17, 0x26)
        #81 = 1000 0001 (F18)
        self.Command(18, 0x81)
        #11 = 0001 0001 (F18)
        self.Command(18, 0x11)
        #AF = 1010 1111 (F1)
        self.Command(1, 0xAF)
        
    #Close the LCD properly
    def Close_LCD(self):
        
        #AE = 1010 1110 (F1)
        self.Command(1, 0xAE)

    #Open the LCD properly
    def Open_LCD(self):

        #AF = 1010 1111 (F1)
        self.Command(1, 0xAF)

    #internal reset with pin
    def Reset(self):
        
        #old /RES pin = "L"
        GPIO.output(17, False)
        #wait 500ms
        sleep(0.5)
        #/RES pin = "H"
        GPIO.output(17, True)
        #Internal reset
        self.Command(14, 0xE2)

    #Clear the LCD
    def Clear(self):
        
        sEmpty = "                                                                                                                                                                        "
        self.Write_text_long(0x00, 0x00, 0x00, sEmpty)

    #Write on the LCD
    def Write(self, start, page, column, data):
        
        if start <= 0x3F:
            
            com_a = 0x40 + start
            self.Command(2, com_a)
            
        else:

            sError = "ERROR: START IS TOO HIGH"
            self.Write_text(0x00, 0x07, 0x00, sError)
            return
            
        if page <= 0x0F:
            
            com_b = 0xB0 + page
            self.Command(3, com_b)
            
        else:
            
            sError = "ERROR: PAGE IS TOO HIGH"
            self.Write_text(0x00, 0x07, 0x00, sError)
            return
            
        com_c, com_d = divmod(column, 0x10)
        
        com_c = com_c + 0x10
        com_d = com_d + 0x00
        
        self.Command(4, com_c)
        self.Command(4, com_d)
        
        #Twelve might be incomplete
        #self.Command(12, 0xE0)
        
        GPIO.output(4, False)
        GPIO.output(27, False)
        
        self.Send_data(0xE0)
        
        GPIO.output(4, True)
        
        for i in range(0, len(data)):
            self.Send_data(data[i])

        GPIO.output(4, False)
        self.Send_data(0xEE)
        GPIO.output(27, True)

    #Write a picture to the LCD
    def Write_picture(self, data):

        self.Write(0x00, 0x07, 0x00, data[:128])
        a = data[128:]
        self.Write(0x00, 0x06, 0x00, a[:128])
        b = a[128:]
        self.Write(0x00, 0x05, 0x00, b[:128])
        c = b[128:]
        self.Write(0x00, 0x04, 0x00, c[:128])
        d = c[128:]
        self.Write(0x00, 0x03, 0x00, d[:128])
        e = d[128:]
        self.Write(0x00, 0x02, 0x00, e[:128])
        f = e[128:]
        self.Write(0x00, 0x01, 0x00, f[:128])
        self.Write(0x00, 0x00, 0x00, f[128:])

    #Write short text to the LCD
    def Write_text(self, start, page, column, text):
        
        if start <= 0x3F:
            
            com_a = 0x40 + start
            self.Command(2, com_a)
            
        else:
            
            sError = "ERROR: START IS TOO HIGH"
            self.Write_text(0x00, 0x07, 0x00, sError)
            return
            
        if page <= 0x0F:
            
            com_b = 0xB0 + page
            self.Command(3, com_b)
            
        else:
            
            sError = "ERROR: PAGE IS TOO HIGH"
            self.Write_text(0x00, 0x07, 0x00, sError)
            return
            
        com_c, com_d = divmod(column, 0x10)
        
        com_c = com_c + 0x10
        com_d = com_d + 0x00
        
        self.Command(4, com_c)
        self.Command(4, com_d)
        
        #Twelve might be incomplete
        #self.Command(12, 0xE0)

        GPIO.output(4, False)
        GPIO.output(27, False)

        self.Send_data(0xE0)
        
        GPIO.output(4, True)
        
        for i in range(0, len(text)):
            for j in range(0,6):
                self.Send_data(ASCII(text[i])[j])
                
        GPIO.output(4, False)
        self.Send_data(0xEE)
        GPIO.output(27, True)

    #Write long text to the LCD
    def Write_text_long(self, start, page, column, text):
        
        if(len(text) < 22):
            self.Write_text(0x00, 0x07, 0x00, text)
        elif(len(text) < 43):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            self.Write_text(0x00, 0x06, 0x00, text[21:])
        elif(len(text) < 64):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            a = text[21:]
            self.Write_text(0x00, 0x06, 0x00, a[:21])
            self.Write_text(0x00, 0x05, 0x00, a[21:])
        elif(len(text) < 85):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            a = text[21:]
            self.Write_text(0x00, 0x06, 0x00, a[:21])
            b = a[21:]
            self.Write_text(0x00, 0x05, 0x00, b[:21])
            self.Write_text(0x00, 0x04, 0x00, b[21:])
        elif(len(text) < 106):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            a = text[21:]
            self.Write_text(0x00, 0x06, 0x00, a[:21])
            b = a[21:]
            self.Write_text(0x00, 0x05, 0x00, b[:21])
            c = b[21:]
            self.Write_text(0x00, 0x04, 0x00, c[:21])
            self.Write_text(0x00, 0x03, 0x00, c[21:])
        elif(len(text) < 127):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            a = text[21:]
            self.Write_text(0x00, 0x06, 0x00, a[:21])
            b = a[21:]
            self.Write_text(0x00, 0x05, 0x00, b[:21])
            c = b[21:]
            self.Write_text(0x00, 0x04, 0x00, c[:21])
            d = c[21:]
            self.Write_text(0x00, 0x03, 0x00, d[:21])
            self.Write_text(0x00, 0x02, 0x00, d[21:])
        elif(len(text) < 148):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            a = text[21:]
            self.Write_text(0x00, 0x06, 0x00, a[:21])
            b = a[21:]
            self.Write_text(0x00, 0x05, 0x00, b[:21])
            c = b[21:]
            self.Write_text(0x00, 0x04, 0x00, c[:21])
            d = c[21:]
            self.Write_text(0x00, 0x03, 0x00, d[:21])
            e = d[21:]
            self.Write_text(0x00, 0x02, 0x00, e[:21])
            self.Write_text(0x00, 0x01, 0x00, e[21:])
        elif(len(text) < 169):
            self.Write_text(0x00, 0x07, 0x00, text[:21])
            a = text[21:]
            self.Write_text(0x00, 0x06, 0x00, a[:21])
            b = a[21:]
            self.Write_text(0x00, 0x05, 0x00, b[:21])
            c = b[21:]
            self.Write_text(0x00, 0x04, 0x00, c[:21])
            d = c[21:]
            self.Write_text(0x00, 0x03, 0x00, d[:21])
            e = d[21:]
            self.Write_text(0x00, 0x02, 0x00, e[:21])
            f = e[21:]
            self.Write_text(0x00, 0x01, 0x00, f[:21])
            self.Write_text(0x00, 0x00, 0x00, f[21:])
        else:
            sError = "ERROR: TEXT TOO LONG"
            self.Write_text(0x00, 0x07, 0x00, sError)

    #function to read from the LCD
    def Read(self):
        
        #TODO
        pass

    #Send_data to the LCD
    def Send_data(self, hexa):
        
        for i in range(0,8):
            
            GPIO.output(23, False)
            
            mask = 1 << (7-i)
            
            if (hexa & mask) > 0:
                
                GPIO.output(24, True)
                
            else:
                
                GPIO.output(24, False)
                
            sleep(0.0000001)
            GPIO.output(23, True)
            sleep(0.0000001)
        
    #Use command to call everysingle function
    def Command(self, number, hexa):

        #Above every function has at least 2 comments :
        # - Command
        # - Function
        
        switch_case = {
        1:self.One,
        2:self.Two,
        3:self.Three,
        4:self.Four,
        5:self.Five,
        6:self.Six,
        7:self.Seven,
        8:self.Eight,
        9:self.Nine,
        10:self.Ten,
        11:self.Eleven,
        12:self.Twelve,
        13:self.Thirteen,
        14:self.Fourteen,
        15:self.Fifteen,
        16:self.Sixteen,
        17:self.Seventeen,
        18:self.Eighteen,
        19:self.Nineteen,
        20:self.Twenty,
        21:self.Twenty_one,
        22:self.Twenty_two
        }
        
        switch_case.get(number, self.Default)(hexa)

    #Display ON/OFF
    #LCD display ON/OFF 0: OFF, 1: ON
    def One(self, hexa):
        
        if hexa == 0xAF or hexa == 0xAE:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Display start line set (0 1 Display start address)
    #Sets the display RAM display start line address
    def Two(self, hexa):
        
        if hexa >= 0x40 or hexa <= 0x7F:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Page address set (1 0 1 1 Page address)
    #Sets the display RAM page address
    def Three(self, hexa):
        
        if hexa >= 0xB0 or hexa <= 0xBF:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #C1: Column address set upper bit (0 0 0 1 Most significant column address)
    #C2: Column address set lower bit (0 0 0 0 Least significant column address)
    #F1: Sets the most significant 4 bits of the display RAM column address
    #F2: Sets the least significant 4 bits of the display RAM column address
    def Four(self, hexa):
        
        if hexa >= 00 or hexa <= 0x1F:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Status read
    #Reads the status data
    def Five(self, hexa):
        
        GPIO.output(4, False)
        GPIO.output(27, False)
        
        status = bus.read_byte(DEVICE_ADDRESS)
        
        GPIO.output(27, True)
        
        return status

    #Display data write
    #Writes to the display RAM
    def Six(self, hexa):
        
        GPIO.output(4, True)
        GPIO.output(27, False)
        
        send_data(hexa)
        
        GPIO.output(27, True)

    #Display data read
    #Reads from the display RAM
    def Seven(self, hexa):
        
        GPIO.output(4, True)
        GPIO.output(27, False)
        
        byte = bus.read_byte(self.DEVICE_ADDRESS)
        
        GPIO.output(27, True)
        
        return byte

    #ADC select
    #Sets the display RAM address SEG output correspondence 0: normal, 1: reverse
    def Eight(self, hexa):
        
        if hexa == 0xA1 or hexa == 0xA0:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Display normal/reverse
    #Sets the LCD display normal/reverse
    def Nine(self, hexa):
        
        if hexa == 0xA7 or hexa == 0xA6:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Display all points ON/OFF
    #DIsplay all points 0: normal display, 1: all points ON
    def Ten(self, hexa):
        
        if hexa == 0xA5 or hexa == 0xA4:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #LCD bias set
    #Sets the LCD drive voltage bias ratio 0: 1/9 bias, 1: 1/7 bias (ST7565)
    def Eleven(self, hexa):
        
        if hexa == 0xA3 or hexa == 0xA2:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Read/modify/write
    #Column address increment At write: +1, At read:0
    def Twelve(self, hexa):
        
        if hexa == 0xE0:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #End
    #Clear red/modify/write
    def Thirteen(self, hexa):
        
        if hexa == 0xEE:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Reset
    #Internal reset
    def Fourteen(self, hexa):
        if hexa == 0xE2:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Common output mode select
    #Select COM output scan direction 0: normal direction, 1: reverse direction
    def Fifteen(self, hexa):
        
        if hexa >= 0xC0 or hexa <= 0xCF:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Power control set
    #Select internal power supply operating mode
    def Sixteen(self, hexa):
        
        if hexa >= 0x28 or hexa <= 0x2F:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #V5 voltage regulator internal resistor ratio set
    #Select internal resistor ratio(Rb/Ra) mode
    def Seventeen(self, hexa):
        
        if hexa >= 0x20 or hexa <= 0x27:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #C1: Electronic volume mode set
    #C2: Electronic volume register set
    #Set the V5 output voltage electronic volume register
    def Eighteen(self, hexa):
        
        if hexa >= 0x00 or hexa <= 0x3F or hexa == 0x81:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #C1: Static indicator ON/OFF
    #C2: Static indicator register set
    #F1: 0: OFF, 1: ON
    #F2: Set the flashing mode
    def Nineteen(self, hexa):
        
        if hexa >= 0x00 or hexa <= 0x03 or hexa == 0xAC or hexa == 0xAD:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Power saver
    #Display OFF and display all points ON compound command
    def Twenty(self, hexa):
        
        #TODO
        pass

    #NOP
    #Command for non-operation
    def Twenty_one(self, hexa):
        
        if hexa == 0xE3:
            
            GPIO.output(4, False)
            GPIO.output(27, False)
            
            self.Send_data(hexa)
            
            GPIO.output(27, True)

    #Test
    #Command for IC test. Do not use this command
    def Twenty_two(hexa):
        
        #command isn't setup since it shouldn't be used
        pass

    #Default
    #Wrong input has been made
    def Default(self, hexa):
        
        print("ERROR with input : {}".format(hexa))