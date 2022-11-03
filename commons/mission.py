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
    def __init__(self, name, robot, paths, logger, shall_trace = False, header='---') :
        """ Contruct mission 1
        ---
        name (str)          : Name of the mission
        robot (obj)         : Initialized robot
        paths (list)        : List of the names of the path to create
        logger(obj)         : Logger to use for log collection
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        header              : Trace header
        """
        super().__init__(name, logger, shall_trace, header)

        self.m_robot            = robot
        self.m_paths            = {}
        for path in paths :
            self.m_paths[path] = Path(self.m_robot, logger, self.m_shall_trace)

# pylint: enable=R0913
