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

class Mission :
    """ Generic mission class """

    m_name         = ''

    m_paths        = {}
    m_robot        = None

    m_shall_trace  = False
    m_trace_header = ''

# pylint: disable=R0913
    def __init__(self, name, robot, paths, shall_trace = False, header='---') :
        """ Contruct mission 1
        ---
        name (str)          : Name of the mission
        robot (obj)         : Initialized robot
        paths (arr)         : List of the names of the path to create
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        header              : Trace header
        """

        self.m_shall_trace      = shall_trace
        self.m_trace_header     = header
        self.m_name             = name
        self.m_robot            = robot
        self.m_paths            = {}
        for path in paths :
            self.m_paths[path] = Path(self.m_robot, shall_trace)


# pylint: enable=R0913

    def log(self, message) :
        """ Log function """

        if self.m_shall_trace : print(self.m_trace_header + message)
