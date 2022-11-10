""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Keywords to create data for module test
# -------------------------------------------------------
# Nadège LEMPERIERE, @1 november 2022
# Latest revision: 1 november 2022
# --------------------------------------------------- """

# Openpyxl includes
from openpyxl import load_workbook

# Robotframework includes
from robot.libraries.BuiltIn import BuiltIn, _Misc
from robot.api import logger as logger
from robot.api.deco import keyword
ROBOT = False

# Mock includes
from spike.context import Context
from spike.truth   import Truth

# Local includes
from mockrobot import MockRobot
from logger import Logger

@keyword('Load Data')
def load_data(configuration, filename, sheet, angle, distance) :

    result = {}

    log = Logger(shall_print_at_once=True)
    logconfig = {'shall_trace':True, 'header':'---'}

    result['context'] = Context()
    result['context'].load_scenario(filename, sheet)
    result['truth'] = Truth()
    result['truth'].load_configuration(configuration)
    result['robot']   = MockRobot()
    result['robot'].setup()

    result['path'] = [{'yaw':float(angle),   'distance':float(distance)}]

    return result
