""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Generic mission code
# -------------------------------------------------------
# Each mission differ, but at some points requires to go there,
# and then move back
# -------------------------------------------------------
# Nadège LEMPERIERE, @19 october 2022
# Latest revision: 19 october 2022
# --------------------------------------------------- """

# Local includes
from commons.logger import ObjectWithLog

class Mission(ObjectWithLog) :
    """ Generic mission class """

    m_paths        = {}
    m_robot        = None

# pylint: disable=R0913
    def __init__(self, name, robot, paths, logger, logconfig) :
        """ Contruct generic mission
        ---
        name (str)          : Name of the mission
        robot (obj)         : Initialized robot
        paths (list)        : List of the names of the path to create
        logger(obj)         : Logger to use for log collection
        logconfig (dict)    : Logger configuration parameters
        """
        super().__init__(name, logger, logconfig)

        self.m_robot            = robot
        self.m_paths            = {}
        for path in paths :
            self.m_paths[path] = Path(self.m_robot, logger, logconfig)

# pylint: enable=R0913
