from KEK420_Utilities import *

clCounter = Counter()

clTk = Tk()
clTk.title("KEK420_Connect")
clTk.minsize(700, 480)

clGUI = GUI_Client(clTk)
clGUI.mainloop()