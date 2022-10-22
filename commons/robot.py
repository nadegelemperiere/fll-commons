""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Generic robot class to ensure the correct functioning
# of common bricks
# -------------------------------------------------------
# Nadège LEMPERIERE, @19 october 2022
# Latest revision: 19 october 2022
# --------------------------------------------------- """

# Spike includes
from spike import PrimeHub, Motor, MotorPair, ColorSensor

class Robot :
    """
    Generic class to share robot information with all python functions
    """

    m_components                = {}
    m_ports                     = {}
    m_hub                       = None

    # Distance between the 2 wheels in centimeters
    m_wheels_distance           = 0
    # Correction to define backward and forward according to motors position
    m_direction                 = 1

    def __init__(self) :
        """ Constructor"""
        self.m_hub                      = None
        self.m_motors                   = {}
        self.m_ports                    = {
            'motor'     : {},
            'color'     : {},
            'distance'  : {},
            'pression'  : {},
        }
        self.m_wheels_distance          = 0
        self.m_direction                = 1

    def initialize(self) :
        """ Robot intialization
        ---
        Initialize all electric components
        Build motor pair if right and left motors exist
        Initialize yaw to 0
        """

        self.m_hub              = PrimeHub()

        if 'color' in self.m_ports :
            self.m_components['color'] = {}
            for name, port in self.m_ports['color'].items():
                self.m_components['color'][name] = ColorSensor(port)

        if 'motor' in self.m_ports :
            self.m_components['motor'] = {}
            for name, port in self.m_ports['motor'].items() :
                self.m_components['motor'][name]  = Motor(port)

            if 'right' in self.m_ports['motor'] and 'left' in self.m_ports['motor'] :
                self.m_components['motor']['pair'] = \
                    MotorPair(self.m_ports['motor']['left'],self.m_ports['motor']['right'])

        self.m_hub.motion_sensor.reset_yaw_angle()

    def get_motor(self, conf) :
        """ Return chosen motors """

        result = None

        if 'motor' in self.m_components and conf in self.m_components['motor'] :
            result = self.m_components['motor'][conf]

        return result

    def get_color_sensor(self,conf) :
        """ Return chosen color sensor """

        result = None

        if 'color' in self.m_components and conf in self.m_components['color'] :
            result = self.m_components['color'][conf]

        return result

    def get_motion_sensor(self) :
        """ Return motion sensor """
        return self.m_hub.motion_sensor

    def get_light_matrix(self) :
        """ Return light matrix """
        return self.m_hub.light_matrix

    def get_wheels_distance(self) :
        """ Return the distance between the wheels in centimeters """
        return self.m_wheels_distance

    def compute_distance(self, distance):
        """ compute distance to set to robot to achieve a given distance"""
        return self.m_direction * distance
