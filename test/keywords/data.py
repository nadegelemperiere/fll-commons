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

# Local includes
from mock import Mock

@keyword('Load Data')
def load_data(filename, sheet, angle, distance) :

    result = {}

    data = load_excel_file(filename,sheet)

    result['robot'] = Mock(data)
    result['robot'].initialize()
    result['path'] = [{'yaw':float(angle),   'distance':float(distance)}]

    return result

def load_excel_file(filename, sheet) :
    """ Load robot fake data from the
        ---
        filename  (str) : Xlsx filename to analyze
        sheet     (str) : Excel sheet in which the cell is located
    """

    result = {}

    full_filename = filename

    # Load workbook with value rather than formula
    wbook = load_workbook(full_filename, data_only = True)

    # Select sheet
    content_sheet = wbook[sheet]

    # Associate header to column
    i_column = 1
    column_to_header = {}
    header_to_column = {}
    content = content_sheet.cell(1,i_column).value
    while content is not None :
        column_to_header[i_column]  = content
        header_to_column[content]   = i_column
        i_column = i_column + 1
        content = content_sheet.cell(1,i_column).value
    if not 'time' in header_to_column : raise Exception('Time column not found')
    if not 'right degrees' in header_to_column : raise Exception('Right motor column not found')
    if not 'left degrees' in header_to_column : raise Exception('Left motor column not found')
    if not 'yaw' in header_to_column : raise Exception('Yaw column not found')

    logger.info(str(header_to_column['yaw']))
    logger.info(str(header_to_column['time']))
    logger.info(str(header_to_column['right degrees']))
    logger.info(str(header_to_column['left degrees']))

	# Parse the lines to build data
    result['yaw'] = []
    result['right'] = []
    result['left'] = []
    result['time'] = []

    for i_row in range(2,content_sheet.max_row + 1) :

        result['yaw'].append(
            float(content_sheet.cell(i_row,header_to_column['yaw']).value))
        result['time'].append(
            float(content_sheet.cell(i_row,header_to_column['time']).value))
        result['right'].append(
            float(content_sheet.cell(i_row,header_to_column['right degrees']).value))
        result['left'].append(
            float(content_sheet.cell(i_row,header_to_column['left degrees']).value))

    return result
