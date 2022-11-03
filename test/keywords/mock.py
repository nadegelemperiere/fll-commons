""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Mock robot providing controlled position information
# -------------------------------------------------------
# Nadège LEMPERIERE, @1 november 2022
# Latest revision: 1 november 2022
# --------------------------------------------------- """


# System includes
from time import time

# Module includes
from commons.robot import Robot
from commons.logger import Logger

class MockTimer :

    m_reference_time = -1

    def __init__(self) :

        self.m_reference_time = time()

    def reset(self) :

        self.m_reference_time = time()


    def now(self) :

        return (time() - self.m_reference_time)

class MockMotionSensor :
    """ Class mocking the gyroscope """

    m_yaw_data = []

    m_current_index = -1

    def __init__(self, data) :
        """ Constructor"""

        self.m_yaw_data             = data
        self.m_current_index        = 0

    def get_yaw_angle(self) :
        return self.m_yaw_data[self.m_current_index]

    def get_roll_angle(self) :
        return 0

    def get_pitch_angle(self) :
        return 0

    def next(self) :
        self.m_current_index += 1
        if self.m_current_index > (len(self.m_yaw_data) - 1) :
            self.m_current_index = len(self.m_yaw_data) - 1


class MockHub :

    motion_sensor = None

    def __init__(self, data) :
        """ Constructor"""

        self.motion_sensor          = MockMotionSensor(data)
        self.m_current_index        = 0

class MockMotor :

    m_degrees_data = []

    m_current_index = -1

    def __init__(self, data) :
        """ Constructor"""

        self.m_degrees_data         = data
        self.m_current_index        = 0

    def get_degrees_counted(self) :
        return self.m_degrees_data[self.m_current_index]

    def next(self) :
        self.m_current_index += 1
        if self.m_current_index > (len(self.m_degrees_data) - 1) :
            self.m_current_index = len(self.m_degrees_data) - 1

class MockMotorPair :

    m_values    = {}

    m_right     = None
    m_left      = None
    m_motion    = None

    def __init__(self, left, right, motion) :
        self.m_values['power'] = []
        self.m_values['steering'] = []
        self.m_right = right
        self.m_left = left
        self.m_motion = motion

    def start_at_power(self, power, steering) :
        self.m_values['power'].append(power)
        self.m_values['steering'].append(steering)
        self.m_right.next()
        self.m_left.next()
        self.m_motion.next()

    def stop(self) :
        yield

    def get_values(self) :
        return self.m_values


class Mock(Robot):
    """ Class to share robot information with all python functions """

    m_data      = {}

    m_timer     = None
    m_logger    = None

    def __init__(self, data) :
        """ Constructor"""
        super().__init__(self.m_logger, True, '---')

        self.m_wheels_distance      = 14.3
        self.m_wheel_diameter       = 8.8
        self.m_data                 = data
        self.m_shall_trace          = True

        self.m_timer    = MockTimer()
        self.m_logger   = Logger(self.m_timer,shall_print_at_once=False)


    def initialize(self) :
        """ Robot intialization
        ---
        Initialize all electric components
        Build motor pair if right and left motors exist
        Initialize yaw to 0
        """

        self.m_hub                          = MockHub(self.m_data['yaw'])
        self.m_components['motor']          = {}
        self.m_components['motor']['right'] = MockMotor(self.m_data['right'])
        self.m_components['motor']['left']  = MockMotor(self.m_data['left'])
        self.m_components['motor']['pair']  = MockMotorPair( \
            self.m_components['motor']['left'] , \
            self.m_components['motor']['right'], \
            self.m_hub.motion_sensor)

