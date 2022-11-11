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

# Commons includes
from commons.logger import Logger
from commons.path import Path

# Mock includes
from spike.context import Context
from spike.truth   import Truth

# Local includes
from mockrobot import MockRobot

@keyword('Load Data')
def load_data(configuration, filename, sheet, angle, distance) :

    result = {}

    log = Logger(shall_print_at_once=True)
    logconfig = {'shall_trace':True, 'header':'---'}

    result['context'] = Context()
    result['context'].load(filename, sheet)
    result['truth'] = Truth()
    result['truth'].load_configuration(configuration)
    result['robot'] = MockRobot(log, logconfig)
    result['robot'].setup()
    result['path'] = [{'yaw':float(angle),   'distance':float(distance)}]

    return result

@keyword('Apply Filter')
def apply_filter(data) :

    log = Logger(shall_print_at_once=True)
    path = Path(data['robot'], log, {'shall_trace':True, 'header':'---'})
    path.set(data['path'])

    gpath = path.start(min_speed=20, ramp=0.2, max_speed=100)
    shall_follow = next(gpath)
    while shall_follow :
        if shall_follow : shall_follow = next(gpath)

    result = data['context'].get_commands()
    print(str(result))
    return result
