""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Keywords to apply filters on position
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

# Module includes
from commons.path import Path
from commons.logger import Logger

@keyword('Apply Filter')
def apply_filter(data) :

    log = Logger(shall_print_at_once=True)
    path = Path(data['robot'], log, {'shall_trace':True, 'header':'---'})
    path.set(data['path'])
    path.start(min_speed=20, ramp=0.2, max_speed=100)
    result = data['robot'].get_motor('pair').get_values()
    print(str(result))
    return result


