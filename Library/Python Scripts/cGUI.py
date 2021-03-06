from gSettings import *
from cTCP import *

#TODO : Do not import has *
from tkinter import *


# @Define   Graphical User Interface (GUI) to connect to a server
#
# @Author   Maxime Lagadec
# @Date     1/13/2018
#
class GUI_Client(Frame) :

    #Variables definition

    sSelected_Action = "Action_?"

    clTCP = TCP(False)

    bIsConnected = False

    # @Define   Initialisation of the class
    # @Define   Launch the GUI
    #
    def __init__(self, master = None):

        Frame.__init__(self, master)

        self.master = master
        self.pack()
        self.CreateWidgets()

        self.bIsConnected = False

    # @Define   GUI frame definition and bindings
    #
    def CreateWidgets(self):

        #Main frame setup
        self.Main = PanedWindow(self, orient = VERTICAL)

        self.Upper_Lair = PanedWindow(self, orient = HORIZONTAL)
        self.Lower_Lair = PanedWindow(self, orient = HORIZONTAL)

        #1st PanedWindow definitions
        self.IP_Menu = PanedWindow(self, orient = VERTICAL)

        self.IP_Menu_Text = Label(self)
        self.IP_Menu_Text["text"] = "\n\tSelect the IP to connect and disconnect from :\t\n"
        self.IP_Menu_Text.pack(fill = X)

        self.IP_Menu_Listbox_IPs = Listbox(self, selectmode = BROWSE)
        self.IP_Menu_Listbox_IPs.insert(END, self.clTCP.sHostIP)
        self.IP_Menu_Listbox_IPs.config(activestyle = "none")
        self.IP_Menu_Listbox_IPs.pack(fill = BOTH)

        self.IP_Menu_Button_Disconnect = Button(self)
        self.IP_Menu_Button_Disconnect["text"] = "Disconnect"
        self.IP_Menu_Button_Disconnect["fg"]   = "red"
        self.IP_Menu_Button_Disconnect.bind("<Button-1>", self.Disconnect)
        self.IP_Menu_Button_Disconnect.pack(fill = X)

        self.IP_Menu_Button_Connect = Button(self)
        self.IP_Menu_Button_Connect["text"] = "Connect"
        self.IP_Menu_Button_Connect["fg"] = "green"
        self.IP_Menu_Button_Connect.bind("<Button-1>", self.Connect)
        self.IP_Menu_Button_Connect.pack(fill = X)
        
        #1st Paned window end (adds and minsizes)
        self.IP_Menu.add(self.IP_Menu_Text)
        self.IP_Menu.paneconfigure(self.IP_Menu_Text, minsize = 30)
        self.IP_Menu.add(self.IP_Menu_Listbox_IPs)
        self.IP_Menu.paneconfigure(self.IP_Menu_Listbox_IPs, minsize = 200)
        self.IP_Menu.add(self.IP_Menu_Button_Connect)
        self.IP_Menu.paneconfigure(self.IP_Menu_Button_Connect, minsize = 30)
        self.IP_Menu.add(self.IP_Menu_Button_Disconnect)
        self.IP_Menu.paneconfigure(self.IP_Menu_Button_Disconnect, minsize = 30)

        #2nd PanedWindow definitions
        self.Connected_Options = PanedWindow(self, orient = VERTICAL)

        self.Connected_Options_Text = Label(self)
        self.Connected_Options_Text["text"] = "\n\tSelect the operation you wish to execute :\t\n"

        self.Connected_Options_Listbox_Actions = Listbox(self, selectmode = BROWSE)
        self.Connected_Options_Listbox_Actions.insert(END, "Send File")
        self.Connected_Options_Listbox_Actions.insert(END, "Receive File")
        self.Connected_Options_Listbox_Actions.insert(END, "Setup Logging")
        self.Connected_Options_Listbox_Actions.insert(END, "Start Logging")
        self.Connected_Options_Listbox_Actions.insert(END, "Stop Logging")

        #Add all user defined actions
        for ACTIONS in ACTIONS_LIST:
            self.Connected_Options_Listbox_Actions.insert(END, ACTIONS[0])

        self.Connected_Options_Listbox_Actions.config(activestyle = "none")
        self.Connected_Options_Listbox_Actions.bind("<<ListboxSelect>>", self.Options)
        self.Connected_Options_Listbox_Actions.pack(fill = BOTH)

        self.Connected_Options_Execute = Button(self)
        self.Connected_Options_Execute["text"] = "Execute"
        self.Connected_Options_Execute["fg"]   = "green"
        self.Connected_Options_Execute.bind("<Button-1>", self.Execute)
        self.Connected_Options_Execute.pack(fill = X)

        self.Connected_Options_Cancel = Button(self)
        self.Connected_Options_Cancel["text"] = "Cancel"
        self.Connected_Options_Cancel["fg"] = "red"
        self.Connected_Options_Cancel.bind("<Button-1>", self.Cancel)
        self.Connected_Options_Cancel.pack(fill = X)

        #2nd Paned window end (adds)
        self.Connected_Options.add(self.Connected_Options_Text)
        self.Connected_Options.paneconfigure(self.Connected_Options_Text, minsize = 30)
        self.Connected_Options.add(self.Connected_Options_Listbox_Actions)
        self.Connected_Options.paneconfigure(self.Connected_Options_Listbox_Actions, minsize = 200)
        self.Connected_Options.add(self.Connected_Options_Execute)
        self.Connected_Options.paneconfigure(self.Connected_Options_Execute, minsize = 30)
        self.Connected_Options.add(self.Connected_Options_Cancel)
        self.Connected_Options.paneconfigure(self.Connected_Options_Cancel, minsize = 30)

        #3rd PanedWindow definitions
        self.File_Argument_Options = PanedWindow(self, orient = VERTICAL)

        self.File_Arguments_Options_Text_A = Label(self)
        self.File_Arguments_Options_Text_A["text"] = "File location on local computer : "
        self.File_Arguments_Options_Text_A.pack(side = "left")
        self.File_Arguments_Options_Entry_A = Entry(self, width = 100)
        self.File_Arguments_Options_Entry_A.pack()

        self.File_Arguments_Options_Text_B = Label(self)
        self.File_Arguments_Options_Text_B["text"] = "File destination on remote computer : "
        self.File_Arguments_Options_Text_B.pack(side = "left")
        self.File_Arguments_Options_Entry_B = Entry(self, width = 100)
        self.File_Arguments_Options_Entry_B.pack()

        #3rd Paned window end (adds)
        self.File_Argument_Options.add(self.File_Arguments_Options_Text_A)
        self.File_Argument_Options.paneconfigure(self.File_Arguments_Options_Text_A, minsize = 30)
        self.File_Argument_Options.add(self.File_Arguments_Options_Entry_A)
        self.File_Argument_Options.paneconfigure(self.File_Arguments_Options_Entry_A, minsize = 30)
        self.File_Argument_Options.add(self.File_Arguments_Options_Text_B)
        self.File_Argument_Options.paneconfigure(self.File_Arguments_Options_Text_B, minsize = 30)
        self.File_Argument_Options.add(self.File_Arguments_Options_Entry_B)
        self.File_Argument_Options.paneconfigure(self.File_Arguments_Options_Entry_B, minsize = 30)

        #4th PanedWindow definitions
        self.Logging_Argument_Options = PanedWindow(self, orient = VERTICAL)

        self.Logging_Arguments_Options_Text_A = Label(self)
        self.Logging_Arguments_Options_Text_A["text"] = "File name : "
        self.Logging_Arguments_Options_Text_A.pack(side = "left")
        self.Logging_Arguments_Options_Entry_A = Entry(self, width = 100)
        self.Logging_Arguments_Options_Entry_A.pack()

        self.Logging_Arguments_Options_Text_B = Label(self)
        self.Logging_Arguments_Options_Text_B["text"] = "File location : "
        self.Logging_Arguments_Options_Text_B.pack(side = "left")
        self.Logging_Arguments_Options_Entry_B = Entry(self, width = 100)
        self.Logging_Arguments_Options_Entry_B.pack()

        #4th Paned window end (adds)
        self.Logging_Argument_Options.add(self.Logging_Arguments_Options_Text_A)
        self.Logging_Argument_Options.paneconfigure(self.Logging_Arguments_Options_Text_A, minsize = 30)
        self.Logging_Argument_Options.add(self.Logging_Arguments_Options_Entry_A)
        self.Logging_Argument_Options.paneconfigure(self.Logging_Arguments_Options_Entry_A, minsize = 30)

        self.Logging_Argument_Options.add(self.Logging_Arguments_Options_Text_B)
        self.Logging_Argument_Options.paneconfigure(self.Logging_Arguments_Options_Text_B, minsize = 30)
        self.Logging_Argument_Options.add(self.Logging_Arguments_Options_Entry_B)
        self.Logging_Argument_Options.paneconfigure(self.Logging_Arguments_Options_Entry_B, minsize = 30)

        #Main frame setup end (adds and pack)
        self.Upper_Lair.add(self.IP_Menu)
        self.Upper_Lair.paneconfigure(self.IP_Menu, minsize = 300)
        self.Main.add(self.Upper_Lair)
        self.Main.paneconfigure(self.Upper_Lair, minsize = 290)
        self.Main.add(self.Lower_Lair)
        self.Main.paneconfigure(self.Lower_Lair, minsize = 120)
        self.Main.pack()

    # @Define   Connect to the selected IP
    #
    # @Return   True : Success, False : Error
    #
    def Connect(self, event):

        #If we are not connected
        if not self.bIsConnected:

            #IP selected from the list
            try:
                self.clTCP.sSelected_IP = self.IP_Menu_Listbox_IPs.get(self.IP_Menu_Listbox_IPs.curselection())
            except:
                print("No IP selected!\n")
                return False

            self.Upper_Lair.add(self.Connected_Options)
            self.Upper_Lair.paneconfigure(self.Connected_Options, minsize = 300)
            self.Upper_Lair.pack()
            self.Lower_Lair.pack()

            self.bIsConnected = True

        #If we are connected
        else:
            print("We are already connected!\n")

        return True

    # @Define   Disconnect from the selected IP
    #
    # @Return   True : Success, False : Error
    #
    def Disconnect(self, event):

        self.clTCP.sSelected_IP = ""

        #If we are connected
        if self.bIsConnected:

            self.Lower_Lair.forget(self.File_Argument_Options)
            self.Lower_Lair.forget(self.Logging_Argument_Options)
            self.Lower_Lair.pack()
            self.Upper_Lair.forget(self.Connected_Options)
            self.Upper_Lair.pack()

            self.bIsConnected = False

        #If we are not connected
        else:
            print("We are not connected!\n")

        return True

    # @Define   Execute the selected action
    #
    def Execute(self, event):

        #If nothing is selected exception
        try:
            sAction = self.Connected_Options_Listbox_Actions.get(self.Connected_Options_Listbox_Actions.curselection())
        except:
            if self.sSelected_Action == "Action_?":
                return False
            else:
                sAction = self.sSelected_Action

        if sAction == "Send File":

            sLocation = self.File_Arguments_Options_Entry_A.get()
            sDestination = self.File_Arguments_Options_Entry_B.get()

            #Bad input
            if sLocation == "" or sDestination == "":
                self.clTCP.PrintTCP("Bad input!\n")
                return False

        if sAction == "Receive File":

            sDestination = self.File_Arguments_Options_Entry_A.get()
            sLocation = self.File_Arguments_Options_Entry_B.get()

            #Bad input
            if sLocation == "" or sDestination == "":
                print("Bad input!\n")
                return False

        if sAction == "Setup Logging":
            sLogFileName = self.Logging_Arguments_Options_Entry_A.get()
            sLogFilePosition = self.Logging_Arguments_Options_Entry_B.get()

            #Bad input
            if sLogFileName == "" or sLogFilePosition == "":
                self.clTCP.PrintTCP("Bad input!\n")
                return False

        self.clTCP.PrintTCP("{0}{1}{2}".format("Executing the following action : ", sAction, " : \n"))

        #Execute method(s) called here
        if sAction == "Send File":
            return self.clTCP.Actions(1, sLocation, sDestination)

        elif sAction == "Receive File":
            return self.clTCP.Actions(2, sLocation, sDestination)

        elif sAction == "Setup Logging":
            return self.clTCP.SetupLogging(sLogFileName, sLogFilePosition)

        elif sAction == "Start Logging":
            return self.clTCP.StartLogging()

        elif sAction == "Stop Logging":
            return self.clTCP.StopLogging()

        else:
            try:
                for ACTIONS in ACTIONS_LIST:
                    if ACTIONS[0] == sAction:
                        getattr(sys.modules[__name__], "%s" % (ACTIONS[0]))(self.clTCP)
            except:
                self.clTCP.PrintTCP("\nCould not find action %s!\n\n" % (sAction))

        return False

    # @Define   Cancel the selected action
    #
    # @TODO
    #
    def Cancel(self, event):

        #Cancel method(s) called here
        return

    # @Define   Update option(s) screen depending on action selection
    #
    def Options(self, event):

        #Get selected action
        try:
            self.sSelected_Action = self.Connected_Options_Listbox_Actions.get(self.Connected_Options_Listbox_Actions.curselection())
            self.Lower_Lair.forget(self.File_Argument_Options)
            self.Lower_Lair.forget(self.Logging_Argument_Options)
        except:
            self.Lower_Lair.pack()
            return

        #Pack GUI depending on action selected
        if self.sSelected_Action == "Send File":
            self.Lower_Lair.add(self.File_Argument_Options)
            self.Lower_Lair.pack()         
        elif self.sSelected_Action == "Receive File":
            self.Lower_Lair.add(self.File_Argument_Options)
            self.Lower_Lair.pack()
        elif self.sSelected_Action == "Setup Logging":
            self.Lower_Lair.add(self.Logging_Argument_Options)
            self.Lower_Lair.pack()
        elif self.sSelected_Action == "Start Logging":
            self.Lower_Lair.pack()
        elif self.sSelected_Action == "Stop Logging":
            self.Lower_Lair.pack()
        else:
            self.Lower_Lair.pack()

# @Define   Graphical User Interface (GUI) to launch a server
#
# @Author   Maxime Lagadec
# @Date     1/13/2018
#
class GUI_Server(Frame) :

    #Variables definition
    bIsConnected = False
    iConnections = 0

    clTCP = TCP(True)

    # @Define   Initialisation of the class
    # @Define   Launch the GUI
    #
    def __init__(self, master = None):

        Frame.__init__(self, master)

        self.master = master
        self.pack()
        self.CreateWidgets()

    # @Define   GUI frame definition and bindings
    #
    def CreateWidgets(self):

        #Main frame setup
        self.Main = PanedWindow(self, orient = VERTICAL)

        #1st PanedWindow definitions
        self.Menu = PanedWindow(self, orient = VERTICAL)
        self.Menu_Button_Disconnect = Button(self, height = 1, width = 25)
        self.Menu_Button_Disconnect["text"] = "Disconnect"
        self.Menu_Button_Disconnect["fg"]   = "red"
        self.Menu_Button_Disconnect.bind("<Button-1>", self.Disconnect)
        self.Menu_Button_Disconnect.pack(fill = X)

        self.Menu_Button_Connect = Button(self, height = 1, width = 25)
        self.Menu_Button_Connect["text"] = "Connect"
        self.Menu_Button_Connect["fg"] = "green"
        self.Menu_Button_Connect.bind("<Button-1>", self.Connect)
        self.Menu_Button_Connect.pack(fill = X)

        #1st Paned window end (adds)
        self.Menu.add(self.Menu_Button_Connect)
        self.Menu.add(self.Menu_Button_Disconnect)

        #Main frame setup end (adds and pack)
        self.Main.add(self.Menu)
        self.Main.pack()

    # @Define   Connect the server
    #
    # @Return   True : Success, False : Error
    #
    def Connect(self, event):

        #If we are not connected
        if not self.bIsConnected:

            #Connection method(s) called here
            if not self.clTCP.Connect():
                print("Could not connect properly!\n")
                return False

            self.bIsConnected = True

        #If we are connected
        else:
            print("We are already connected!\n")

        return True

    # @Define   Disconnect the server and all it's connections
    #
    # @Return   True : Success, False : Error
    #
    def Disconnect(self, event):

        #If we are connected
        if self.bIsConnected:

            #Disconnection method(s) called here
            if not self.clTCP.Disconnect():
                print("Could not disconnect properly!\n")
                return False

            self.bIsConnected = False

        #If we are not connected
        else:
            print("We are not connected!\n")

        return True