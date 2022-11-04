""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Class managing PID filtering
# -------------------------------------------------------
# Nadège LEMPERIERE, @10 october 2022
# Latest revision: 10 october 2022
# --------------------------------------------------- """

from commons.logger import ObjectWithLog

# pylint: disable=R0902
class CorrectorPID(ObjectWithLog) :
    """ Corrector (Proportional, Integral, Derivative) """


    m_target                    = 0
    m_tolerance                 = 0
    m_is_angle                  = False

    m_kp                        = 0
    m_ki                        = 0
    m_kd                        = 0

    m_integral                  = 0
    m_last_error                = 0

# pylint: disable=R0913
    def __init__(self, kp, ki, kd, is_angle, logger, logconfig) :
        """ Initialize orienter
        ---
        ki (float)          : Integral coefficient
        kd (float)          : Derivative coefficient
        kp (float)          : Proportional coefficient
        is_angle (bool)     : True if measure is an angle who requires modulo, false otherwise
        logger(obj)         : Logger to use for logs collection
        logconfig (dict)    : Logger configuration parameters
        """

        super().__init__('CorrectorPID', logger, logconfig)

        self.log('Starting PID creation')

        self.m_ki           = ki
        self.m_kd           = kd
        self.m_kp           = kp
        self.m_integral     = 0
        self.m_last_error   = 0
        self.m_target       = 0
        self.m_tolerance    = 0
        self.m_is_angle     = is_angle

        self.log('Ending PID creation')
# pylint: enable=R0913

    def initialize(self, target, tolerance) :
        """ Update the filter with the target value
        ---
        target (float)      : The target value to reach with the filter
        tolerance (float)   : The precision with which the target shall be reached
        """

        self.m_target       = target
        self.m_tolerance    = tolerance

    def update(self, measure) :
        """ Update the filter with the measured value
        ---
        measure (float)     : The measured value to use to update the filter
        ---
        return              : Correction to apply
        """

        result = 0

        error = measure - self.m_target
        if self.m_is_angle and error <= -180 : error += 360
        if self.m_is_angle and error > 180 : error -= 360


        if abs(error) < self.m_tolerance : self.m_integral = 0
        else : self.m_integral += error

        derivative = error - self.m_last_error
        self.m_last_error = error

        result = - (self.m_kp * error + self.m_ki * self.m_integral + self.m_kd * derivative)

        self.log('Current measure : ' + str(measure) + \
            ' Current error : ' + str(error) + \
            ' Current command : ' + str(result))

        return result

# pylint: enable=R0902
