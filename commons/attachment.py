""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Generic attachment class to ensure the correct functioning
# of common bricks
# -------------------------------------------------------
# Nadège LEMPERIERE, @19 october 2022
# Latest revision: 19 october 2022
# --------------------------------------------------- """

# Local includes
from commons.logger import ObjectWithLog

class Attachment(ObjectWithLog) :
    """
    Generic class to share attachment information with all python functions
    """

    m_position = 'front'

    def __init__(self, position, logger, logconfig) :
        """ Constructor
        ---
        position (str)      : Position of the attachment on the robot
        logger (obj)        : Logger to use for log collection
        logconfig (dict)    : Logger configuration parameters
        """
        super().__init__('Attachment', logger, logconfig)

        self.m_position = position

    def get_position(self) :
        """ position return function """
        return self.m_position
