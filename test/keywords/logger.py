""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Keywords to create data for module test
# -------------------------------------------------------
# Nadège LEMPERIERE, @1 november 2022
# Latest revision: 1 november 2022
# --------------------------------------------------- """

# System includes
from time import time

# Robotframework includes
from robot.libraries.BuiltIn import BuiltIn, _Misc
from robot.api import logger as logger
from robot.api.deco import keyword
ROBOT = False

# Module includes
from commons.logger import Logger

@keyword('Log And Print During 100 Iterations')
def log_and_print_during_a_hundred_iterations() :

    result = []

    log = Logger(shall_print_at_once=True)

    initial_time = time()
    current_time = initial_time
    i_iteration = 0

    while i_iteration < 100 :
        current_time = time()
        result.append(current_time - initial_time)
        log.log('---','test','A looooooooooooooooooooooooooooooooooooooooooooooooooooooooong message')
        i_iteration = i_iteration + 1

    return result

@keyword('Log And Retain During 100 Iterations')
def log_and_retain_during_a_hundred_iterations() :

    result = []

    logger = Logger(shall_print_at_once=False)

    initial_time = time()
    current_time = initial_time
    i_iteration = 0

    while i_iteration < 100 :
        current_time = time()
        result.append(current_time - initial_time)
        logger.log('---','test','A looooooooooooooooooooooooooooooooooooooooooooooooooooooooong message')
        i_iteration = i_iteration + 1

    return result

@keyword('Log Selected Topics During 100 Iterations')
def log_selected_topics_during_a_hundred_iterations(topics) :

    result = None

    logger = Logger(shall_print_at_once=False,topics=topics)

    i_iteration = 0

    while i_iteration < 100 :
        logger.log('---','test','A looooooooooooooooooooooooooooooooooooooooooooooooooooooooong message')
        i_iteration = i_iteration + 1

    logger.summarize()
    with open('logs.txt','r') as fid :
        result = fid.read()

    return result

@keyword('Compute Logging Speed')
def compute_logging_speed(result) :

    speed = 100 /result[len(result) - 1]
    return speed
