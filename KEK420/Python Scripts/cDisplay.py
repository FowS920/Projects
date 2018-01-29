from cLCD import *

# @Define   Class used to control the display of the LCD
#
# @Author   Maxime Lagadec
# @Date     7/20/2017
#
# @Note     This class only works on the Raspberry PI
# @Note     LCD is the NHD-C12864A1Z-FSRGB-FBW-HT1
#
# @TODO
#
class Display:

    def __init__(self):

        #TODO
        self.clLCD = LCD()

    def __del__(self):

        #TODO
        pass

    #When the display starts
    def Openning_sequence(self):

        for gif in range(0,3):
            
            self.clLCD.Write_picture(self.dataTankA)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankB)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankC)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankD)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankE)
            sleep(0.3)
            self.clLCD.Write_picture(self.dataTankD)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankC)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankB)
            sleep(0.1)
            self.clLCD.Write_picture(self.dataTankA)
            sleep(0.5)

        self.clLCD.Clear()

    #When the display ends
    def Closing_sequence(self):

        sExitText = "      Goodbye!"
        
        self.clLCD.Clear()
        self.clLCD.Write_text(0x00, 0x04,0x00, sExitText)
        
        sleep(3)

    def Main_sequence(self):

        #TODO
        pass

    #Data storage of pictures
    
    #Tank gif A
    dataTankA = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x01, 0x00,0x02,0x03,0x03,0x07,0x03,0x03,0x03,0x07,0x0F,0x03,0x0D,0x0E,0x0E,0x0E,0x0E, 0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x06,0x07,0x07,0x03,0x03,0x01,0x01,0x01,0x00, 0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x01,0x01,0x01,0x00,0x00,0x00,0x02,0x02, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x03,0x03,0x03,0x03,0x03,0x0F,0x0F,0x0F,0x0F, 0x0F,0x0F,0x0F,0x17,0x1B,0x1F,0x1D,0x1F,0x3F,0x7F,0x7F,0xFF,0xFF,0xFF,0xBF,0x7F, 0xFF,0xFF,0xFF,0xFF,0xFE,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0xFF,0x7F, 0xF1,0x07,0x1F,0x07,0x0F,0x1F,0x17,0x17,0x17,0xD7,0xF7,0x7F,0xFF,0xFF,0xFF,0x7F, 0xEF,0xDF,0x7F,0xDF,0xD0,0x50,0xD0,0x90,0x50,0xF0,0x20,0x60,0x60,0x60,0xE0,0xC0, 0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x1C,0x1E,0x16,0x3E,0x3E,0x3E,0x3E,0x36,0x3E,0x3E,0x3E,0x34, 0x34,0x24,0x34,0x7C,0x6C,0x6C,0x68,0x68,0x68,0x68,0x68,0xD8,0xD8,0xD8,0xD0,0xF0, 0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xC0,0xE0,0xE0, 0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE3,0xE7,0xEF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFC,0xFC,0xFC,0xFC,0xFC,0xF8,0xF8,0xF8,0xF8,0xF8,0xB8,0x88, 0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x02,0x05,0x05,0x0E,0x0E,0x1F,0x07,0x03, 0x1D,0x3C,0x2C,0x2C,0x2C,0x6C,0x6C,0x6C,0x78,0x78,0x48,0xD9,0xCB,0xDF,0xBF,0xFF, 0x7F,0x7F,0x7F,0x7F,0x7F,0x5F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC,0xEF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xF8,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xDF,0xDF,0x6D,0x6C,0x68, 0x68,0x6C,0x6C,0x2C,0x28,0x28,0x34,0x34,0x34,0x14,0x11,0x03,0x0F,0x0E,0x0F,0x05, 0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x28,0x28,0x48,0xB8,0x7C,0xFC,0xEC,0x48,0x98,0x38,0x38,0xB8,0xB8, 0x38,0x38,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3E,0x7E,0xFC,0xFC,0xFE,0xC6,0xD6,0x76, 0x76,0x77,0x7F,0x7B,0x3B,0x3B,0xB7,0xBF,0xBF,0xFF,0xBF,0xFF,0x1F,0xE5,0xFE,0x1B, 0xC7,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0x00,0x38,0xED,0x96,0xD9, 0xFC,0xBF,0xBF,0xB7,0xBB,0xB9,0x9B,0x1B,0x1B,0x73,0x23,0xF3,0x66,0xF6,0xFE,0x7C, 0x3E,0x3E,0x7C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0xBC,0xBC,0xBC,0x1C,0x1C,0xCC,0xC4, 0xA4,0x5C,0x2C,0x9C,0x44,0x24,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xF0,0x0C,0xFE,0x00,0xFE, 0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0x00,0xF0,0x0C,0xCC, 0x00,0x80,0xC0,0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

    #Tank gif B
    dataTankB = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x01, 0x00,0x02,0x03,0x03,0x07,0x03,0x03,0x03,0x07,0x0F,0x03,0x0D,0x0E,0x0E,0x0E,0x0E, 0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x06,0x07,0x07,0x03,0x03,0x01,0x01,0x01,0x00, 0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x01,0x01,0x01,0x00,0x00,0x00,0x02,0x02, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x03,0x03,0x03,0x03,0x03,0x0F,0x0F,0x0F,0x0F, 0x0F,0x0F,0x0F,0x17,0x1B,0x1F,0x1D,0x1F,0x3F,0x7F,0x7F,0xFF,0xFF,0xFF,0xBF,0x7F, 0xFF,0xFF,0xFF,0xFF,0xFE,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0xFF,0x7F, 0xF1,0x07,0x1F,0x07,0x0F,0x1F,0x17,0x17,0x17,0xD7,0xF7,0x7F,0xFF,0xFF,0xFF,0x7F, 0xEF,0xDF,0x7F,0xDF,0xD0,0x50,0xD0,0x90,0x50,0xF0,0x20,0x60,0x60,0x60,0xE0,0xC0, 0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x1C,0x1E,0x16,0x3E,0x3E,0x3E,0x3E,0x36, 0x3E,0x3E,0x3E,0x34,0x34,0x24,0x34,0x7C,0x6C,0x6C,0x68,0xD8,0xD8,0xD8,0xD0,0xF0, 0xF0,0xF0,0xF0,0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xC0,0xE0,0xE0, 0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE3,0xE7,0xEF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFC,0xFC,0xFC,0xFC,0xFC,0xF8,0xF8,0xF8,0xF8,0xF8,0xB8,0x88, 0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x02,0x05,0x05,0x0E,0x0E,0x1F,0x07,0x03, 0x1D,0x3C,0x2C,0x2C,0x2C,0x6C,0x6C,0x6C,0x78,0x78,0x48,0xD9,0xCB,0xDF,0xBF,0xFF, 0x7F,0x7F,0x7F,0x7F,0x7F,0x5F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC,0xEF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xF8,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xDF,0xDF,0x6D,0x6C,0x68, 0x68,0x6C,0x6C,0x2C,0x28,0x28,0x34,0x34,0x34,0x14,0x11,0x03,0x0F,0x0E,0x0F,0x05, 0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x28,0x28,0x48,0xB8,0x7C,0xFC,0xEC,0x48,0x98,0x38,0x38,0xB8,0xB8, 0x38,0x38,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3E,0x7E,0xFC,0xFC,0xFE,0xC6,0xD6,0x76, 0x76,0x77,0x7F,0x7B,0x3B,0x3B,0xB7,0xBF,0xBF,0xFF,0xBF,0xFF,0x1F,0xE5,0xFE,0x1B, 0xC7,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0x00,0x38,0xED,0x96,0xD9, 0xFC,0xBF,0xBF,0xB7,0xBB,0xB9,0x9B,0x1B,0x1B,0x73,0x23,0xF3,0x66,0xF6,0xFE,0x7C, 0x3E,0x3E,0x7C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0xBC,0xBC,0xBC,0x1C,0x1C,0xCC,0xC4, 0xA4,0x5C,0x2C,0x9C,0x44,0x24,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xF0,0x0C,0xFE,0x00,0xFE, 0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0x00,0xF0,0x0C,0xCC, 0x00,0x80,0xC0,0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

    #Tank gif C
    dataTankC = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x01, 0x00,0x02,0x03,0x03,0x07,0x03,0x03,0x03,0x07,0x0F,0x03,0x0D,0x0E,0x0E,0x0E,0x0E, 0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x06,0x07,0x07,0x03,0x03,0x01,0x01,0x01,0x00, 0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x01,0x01,0x01,0x00,0x00,0x00,0x02,0x02, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x01,0x01,0x01,0x01,0x01,0x01,0x03,0x03,0x03,0x03,0x03,0x0F,0x0F,0x0F,0x0F, 0x0F,0x0F,0x0F,0x17,0x1B,0x1F,0x1D,0x1F,0x3F,0x7F,0x7F,0xFF,0xFF,0xFF,0xBF,0x7F, 0xFF,0xFF,0xFF,0xFF,0xFE,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0xFF,0x7F, 0xF1,0x07,0x1F,0x07,0x0F,0x1F,0x17,0x17,0x17,0xD7,0xF7,0x7F,0xFF,0xFF,0xFF,0x7F, 0xEF,0xDF,0x7F,0xDF,0xD0,0x50,0xD0,0x90,0x50,0xF0,0x20,0x60,0x60,0x60,0xE0,0xC0, 0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x38,0x3C, 0x2C,0x7C,0x7C,0x7C,0x7C,0x6C,0x7C,0x7C,0x7C,0x68,0x68,0x48,0x68,0xF8,0xD8,0xD8, 0xD0,0xF0,0xF0,0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xC0,0xE0,0xE0, 0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE3,0xE7,0xEF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFC,0xFC,0xFC,0xFC,0xFC,0xF8,0xF8,0xF8,0xF8,0xF8,0xB8,0x88, 0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x02,0x05,0x05,0x0E,0x0E,0x1F,0x07,0x03, 0x1D,0x3C,0x2C,0x2C,0x2C,0x6C,0x6C,0x6C,0x78,0x78,0x48,0xD9,0xCB,0xDF,0xBF,0xFF, 0x7F,0x7F,0x7F,0x7F,0x7F,0x5F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC,0xEF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xF8,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xDF,0xDF,0x6D,0x6C,0x68, 0x68,0x6C,0x6C,0x2C,0x28,0x28,0x34,0x34,0x34,0x14,0x11,0x03,0x0F,0x0E,0x0F,0x05, 0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x28,0x28,0x48,0xB8,0x7C,0xFC,0xEC,0x48,0x98,0x38,0x38,0xB8,0xB8, 0x38,0x38,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3E,0x7E,0xFC,0xFC,0xFE,0xC6,0xD6,0x76, 0x76,0x77,0x7F,0x7B,0x3B,0x3B,0xB7,0xBF,0xBF,0xFF,0xBF,0xFF,0x1F,0xE5,0xFE,0x1B, 0xC7,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0x00,0x38,0xED,0x96,0xD9, 0xFC,0xBF,0xBF,0xB7,0xBB,0xB9,0x9B,0x1B,0x1B,0x73,0x23,0xF3,0x66,0xF6,0xFE,0x7C, 0x3E,0x3E,0x7C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0xBC,0xBC,0xBC,0x1C,0x1C,0xCC,0xC4, 0xA4,0x5C,0x2C,0x9C,0x44,0x24,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xF0,0x0C,0xFE,0x00,0xFE, 0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0x00,0xF0,0x0C,0xCC, 0x00,0x80,0xC0,0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

    #Tank gif D
    dataTankD = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x01, 0x00,0x02,0x03,0x03,0x07,0x03,0x03,0x03,0x07,0x0F,0x03,0x0D,0x0E,0x0E,0x0E,0x0E, 0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x06,0x07,0x07,0x03,0x03,0x01,0x01,0x01,0x00, 0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x01,0x01,0x01,0x00,0x00,0x00,0x02,0x02, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x01,0x01,0x01,0x01,0x01,0x03,0x03,0x03,0x03,0x03,0x0F,0x0F,0x0F,0x0F, 0x0F,0x0F,0x0F,0x17,0x1B,0x1F,0x1D,0x1F,0x3F,0x7F,0x7F,0xFF,0xFF,0xFF,0xBF,0x7F, 0xFF,0xFF,0xFF,0xFF,0xFE,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0xFF,0x7F, 0xF1,0x07,0x1F,0x07,0x0F,0x1F,0x17,0x17,0x17,0xD7,0xF7,0x7F,0xFF,0xFF,0xFF,0x7F, 0xEF,0xDF,0x7F,0xDF,0xD0,0x50,0xD0,0x90,0x50,0xF0,0x20,0x60,0x60,0x60,0xE0,0xC0, 0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x70,0x78,0x58,0xF8,0xF8,0xF8,0xF8,0xD8,0xF8,0xF8,0xF8,0xD0,0xD0, 0x90,0xD0,0xF0,0xB0,0xB0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xC0,0xE0,0xE0, 0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE3,0xE7,0xEF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFC,0xFC,0xFC,0xFC,0xFC,0xF8,0xF8,0xF8,0xF8,0xF8,0xB8,0x88, 0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x02,0x05,0x05,0x0E,0x0E,0x1F,0x07,0x03, 0x1D,0x3C,0x2C,0x2C,0x2C,0x6C,0x6C,0x6C,0x78,0x78,0x48,0xD9,0xCB,0xDF,0xBF,0xFF, 0x7F,0x7F,0x7F,0x7F,0x7F,0x5F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC,0xEF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xF8,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xDF,0xDF,0x6D,0x6C,0x68, 0x68,0x6C,0x6C,0x2C,0x28,0x28,0x34,0x34,0x34,0x14,0x11,0x03,0x0F,0x0E,0x0F,0x05, 0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x28,0x28,0x48,0xB8,0x7C,0xFC,0xEC,0x48,0x98,0x38,0x38,0xB8,0xB8, 0x38,0x38,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3E,0x7E,0xFC,0xFC,0xFE,0xC6,0xD6,0x76, 0x76,0x77,0x7F,0x7B,0x3B,0x3B,0xB7,0xBF,0xBF,0xFF,0xBF,0xFF,0x1F,0xE5,0xFE,0x1B, 0xC7,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0x00,0x38,0xED,0x96,0xD9, 0xFC,0xBF,0xBF,0xB7,0xBB,0xB9,0x9B,0x1B,0x1B,0x73,0x23,0xF3,0x66,0xF6,0xFE,0x7C, 0x3E,0x3E,0x7C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0xBC,0xBC,0xBC,0x1C,0x1C,0xCC,0xC4, 0xA4,0x5C,0x2C,0x9C,0x44,0x24,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xF0,0x0C,0xFE,0x00,0xFE, 0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0x00,0xF0,0x0C,0xCC, 0x00,0x80,0xC0,0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)

    #Tank gif E
    dataTankE = (0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x04,0x02,0x03,0x19,0x0C,0x06,0x03,0x01,0x00,0x00,0x1E,0x03,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x03,0x01, 0x00,0x02,0x03,0x03,0x07,0x03,0x03,0x03,0x07,0x0F,0x03,0x0D,0x0E,0x0E,0x0E,0x0E, 0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x0E,0x06,0x07,0x07,0x03,0x03,0x01,0x01,0x01,0x00, 0x00,0x00,0x00,0x00,0x01,0x00,0x01,0x00,0x01,0x01,0x01,0x00,0x00,0x00,0x02,0x02, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x01,0x05,0x14,0x12,0x12,0x92,0xD2,0x5A,0x7E,0xBE,0xFF,0x7F,0x0F,0xE7,0x3F,0x0F, 0x03,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x01,0x01,0x01,0x01,0x01,0x03,0x03,0x03,0x03,0x03,0x0F,0x0F,0x0F,0x0F, 0x0F,0x0F,0x0F,0x17,0x1B,0x1F,0x1D,0x1F,0x3F,0x7F,0x7F,0xFF,0xFF,0xFF,0xBF,0x7F, 0xFF,0xFF,0xFF,0xFF,0xFE,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0x7F,0xFF,0x7F, 0xF1,0x07,0x1F,0x07,0x0F,0x1F,0x17,0x17,0x17,0xD7,0xF7,0x7F,0xFF,0xFF,0xFF,0x7F, 0xEF,0xDF,0x7F,0xDF,0xD0,0x50,0xD0,0x90,0x50,0xF0,0x20,0x60,0x60,0x60,0xE0,0xC0, 0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x88,0x98,0x91,0xB3,0xF6,0xF4,0xFC,0xF9,0xFB,0x7B,0x77,0xFF,0xFF,0xFF,0xFE, 0xFE,0xFC,0x00,0x70,0x78,0x58,0xF8,0xF8,0xF8,0xF8,0xD8,0xF8,0xF8,0xF8,0xD0,0xD0, 0x90,0xD0,0xF0,0xB0,0xB0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xE0,0xC0,0xE0,0xE0, 0xF0,0xF0,0xF0,0xE0,0xE0,0xE0,0xE0,0xE3,0xE7,0xEF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0x9F,0x7F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFC,0xFC,0xFC,0xFC,0xFC,0xF8,0xF8,0xF8,0xF8,0xF8,0xB8,0x88, 0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x8C,0x18,0x11,0x37,0x6E,0xDE,0xFC,0xD8,0xF0,0x8C,0xB8,0xE0,0x80, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x01,0x02,0x05,0x05,0x0E,0x0E,0x1F,0x07,0x03, 0x1D,0x3C,0x2C,0x2C,0x2C,0x6C,0x6C,0x6C,0x78,0x78,0x48,0xD9,0xCB,0xDF,0xBF,0xFF, 0x7F,0x7F,0x7F,0x7F,0x7F,0x5F,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFC,0xEF, 0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFF,0xFE,0xF8,0xFF,0xFF,0xFF, 0xFF,0xFF,0xFF,0xFF,0xFF,0x7F,0x7F,0x7F,0x7F,0x7F,0xFF,0xDF,0xDF,0x6D,0x6C,0x68, 0x68,0x6C,0x6C,0x2C,0x28,0x28,0x34,0x34,0x34,0x14,0x11,0x03,0x0F,0x0E,0x0F,0x05, 0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0xC0,0x80,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x28,0x28,0x48,0xB8,0x7C,0xFC,0xEC,0x48,0x98,0x38,0x38,0xB8,0xB8, 0x38,0x38,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3E,0x7E,0xFC,0xFC,0xFE,0xC6,0xD6,0x76, 0x76,0x77,0x7F,0x7B,0x3B,0x3B,0xB7,0xBF,0xBF,0xFF,0xBF,0xFF,0x1F,0xE5,0xFE,0x1B, 0xC7,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0xDF,0x00,0x38,0xED,0x96,0xD9, 0xFC,0xBF,0xBF,0xB7,0xBB,0xB9,0x9B,0x1B,0x1B,0x73,0x23,0xF3,0x66,0xF6,0xFE,0x7C, 0x3E,0x3E,0x7C,0x3C,0x3C,0x3C,0x3C,0x3C,0x3C,0xBC,0xBC,0xBC,0x1C,0x1C,0xCC,0xC4, 0xA4,0x5C,0x2C,0x9C,0x44,0x24,0x14,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0xC0,0xC0,0xC0,0xC0,0xC0,0xC0,0xF0,0x0C,0xFE,0x00,0xFE, 0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0xFE,0x00,0xF0,0x0C,0xCC, 0x00,0x80,0xC0,0xC0,0xC0,0x80,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,
              0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00, 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00)