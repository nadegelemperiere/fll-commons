""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Mock robot providing controlled position information
# -------------------------------------------------------
# Nadège LEMPERIERE, @1 november 2022
# Latest revision: 1 november 2022
# --------------------------------------------------- """

# Module includes
from commons.spikebot   import Spikebot

class MockRobot(Spikebot):

    """ Class to share robot information with all python functions """

    def __init__(self, logger, logconfig) :
        """ Constructor
        ---
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        logconfig (dict)    : Logger configuration parameters
        """

        super().__init__(logger, logconfig)

        self.m_wheels_distance      = 14.3
        self.m_wheel_diameter       = 8.8
        self.m_ports                = {
            'motor' : { 'right' : 'E', 'left' : 'F' }
        }

    def setup(self) :
        """ Overloaded initialization function to manage attachments """
        super().setup()
