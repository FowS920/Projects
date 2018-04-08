# @Define   Projects Settings
#
# @Author   Maxime Lagadec
# @Date     2/17/2018
#
# @Usage    Create your own Project Settings and import gSettings.py
# @Usage    Then redefine the global variables according to their usage
# @Usage    Make sure to modify the IMPORT_SPECIFIC_FUNCTIONS for your project
#
# @Note     Use this file to declare projects settings (declare GLOBALs)
# @Note     Use this file to import specific functions from projects
#

#Declare settings
global CURRENT_PROJECT
CURRENT_PROJECT = "UNKNOWN"
global NULL
NULL = 0

# @Define   List of project specific actions
#
# @Usage    Every function must have exactly one input :
# @Usage    TCP class to be able to communicate with Host or Slave
#
# @Usage    Use ACTIONS_LIST.append(["NameOfFunction", FunctionNumber])
#
# @Note     FunctionNumber must be above or equal to 1000
# @Note     Use the TCP class to determine if you are host or slave
# @Note     See variable bTCPHost inside cTCP.py
#
# @Example  There is an example function inside file fExample.py
#
global ACTIONS_LIST
ACTIONS_LIST = []

# @Define   Depending on CURRENT_PROJECT import different functions
#
# @Usage    List all the file you want to import (usually functions)
#
def IMPORT_SPECIFIC_FUNCTIONS():

    if CURRENT_PROJECT == "KEK420":

        #TODO
        pass

    if CURRENT_PROJECT == "UNKNOWN":

        #TODO
        pass