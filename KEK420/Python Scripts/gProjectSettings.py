# @Define   Project Settings
#
# @Author   Maxime Lagadec
# @Date     2/17/2018
#
# @Note     Use this file to define projects settings (define GLOBALs)
#

import gSettings as SETTINGS

#All functions will require TCP
from cTCP import *

#Set settings
SETTINGS.CURRENT_PROJECT = "KEK420"

#Add functions
SETTINGS.ACTIONS_LIST.append(["Function_A", 1000])
SETTINGS.ACTIONS_LIST.append(["Function_B", 1001])
SETTINGS.ACTIONS_LIST.append(["Function_C", 1002])
SETTINGS.ACTIONS_LIST.append(["Function_D", 1003])
SETTINGS.ACTIONS_LIST.append(["Function_E", 1004])
SETTINGS.ACTIONS_LIST.append(["Function_F", 1005])
SETTINGS.ACTIONS_LIST.append(["Function_G", 1006])
SETTINGS.ACTIONS_LIST.append(["Function_H", 1007])
SETTINGS.ACTIONS_LIST.append(["Function_I", 1008])
SETTINGS.ACTIONS_LIST.append(["Function_J", 1009])
SETTINGS.ACTIONS_LIST.append(["Function_K", 1010])
SETTINGS.ACTIONS_LIST.append(["Function_L", 1011])
SETTINGS.ACTIONS_LIST.append(["Function_M", 1012])
SETTINGS.ACTIONS_LIST.append(["Function_N", 1013])
SETTINGS.ACTIONS_LIST.append(["Function_O", 1014])
SETTINGS.ACTIONS_LIST.append(["Function_P", 1015])
SETTINGS.ACTIONS_LIST.append(["Function_Q", 1016])
SETTINGS.ACTIONS_LIST.append(["Function_R", 1017])
SETTINGS.ACTIONS_LIST.append(["Function_S", 1018])

#Depending on settings import different functions
SETTINGS.IMPORT_SPECIFIC_FUNCTIONS()