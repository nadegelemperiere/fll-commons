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

# Local includes
from math import pi

# Spike includes
from spike import PrimeHub, Motor, MotorPair, ColorSensor

class Spikebot(Robot) :
    """
    Generic class to share spike robot information with all python functions
    """

    def __init__(self,  logger, logconfig) :
        """ Constructor
        ---
        logger (obj)        : Logger to use for log collection
        logconfig (dict)    : Logger configuration parameters
        """
        super().__init__(logger, logconfig)

        self.m_hub              = PrimeHub()

    def initialize(self) :
        """ Robot intialization
        ---
        Initialize all electric components
        Build motor pair if right and left motors exist
        Initialize yaw to 0
        """

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
        self.m_components['motor']['pair'].set_motor_rotation(self.m_wheel_diameter * pi, 'cm')
