""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# High resolution timer with a milliseconds resolution
# emulating spike timer interfaces on micropython
# -------------------------------------------------------
# Nadège LEMPERIERE, @04 november 2022
# Latest revision: 04 november 2022
# --------------------------------------------------- """

# System includes
from utime import ticks_diff, ticks_ms

class UTimer :
    """ Milliseconds timer on micropython """

    m_start_ticks = 0

    def __init__(self) :
        """ Constructor """
        self.m_start_ticks = 0

    def now(self) :
        """ Current time return function """
        result = 1.0 * ticks_diff(ticks_ms(),self.m_start_ticks) / 1000
        return result

    def reset(self):
        """ Time reset function """
        self.m_start_ticks = ticks_ms()
