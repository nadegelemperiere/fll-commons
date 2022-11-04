""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# High resolution timer with a milliseconds resolution
# emulating spike timer interfaces on standard python
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from time import time

class UTimer :
    """ Milliseconds timer on standard python """

    m_reference_time = -1

    def __init__(self) :
        """ Constructor """
        self.m_reference_time = time()

    def now(self) :
        """ Current time return function """
        return time() - self.m_reference_time

    def reset(self) :
        """ Time reset function """
        self.m_reference_time = time()
