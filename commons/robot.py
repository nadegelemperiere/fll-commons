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
from commons.logger import ObjectWithLog

class Robot(ObjectWithLog) :
    """
    Generic class to share robot information with all python functions
    """

    m_components                = {}
    m_ports                     = {}
    m_attachments               = {}
    m_hub                       = None

    # Distance between the 2 wheels in centimeters
    m_wheels_distance           = 0
    # Wheel diameter in centimers
    m_wheel_diameter            = 0
    # Correction to define backward and forward according to motors position
    m_direction                 = 1

    def __init__(self,  logger, shall_trace = False, header='---') :
        """ Constructor
        ---
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        logger (obj)        : Logger to use for log collection
        header              : Trace header
        """
        super().__init__('Robot', logger, shall_trace, header)

        self.m_hub                      = None
        self.m_motors                   = {}
        self.m_ports                    = {
            'motor'     : {},
            'color'     : {},
            'distance'  : {},
            'pression'  : {},
        }
        self.m_wheels_distance          = 0
        self.m_wheel_diameter           = 0
        self.m_attachments              = {}

    def get_motor(self, conf) :
        """ Return chosen motors
        ---
        conf (str)      : Name of the motor to get
        ---
        returns (obj)   : The motor
        """

        result = None

        if 'motor' in self.m_components and conf in self.m_components['motor'] :
            result = self.m_components['motor'][conf]

        return result

    def get_color_sensor(self,conf) :
        """ Return chosen color sensor
        ---
        conf (str)      : Name of the sensor to get
        ---
        returns (obj)   : The sensor
        """

        result = None

        if 'color' in self.m_components and conf in self.m_components['color'] :
            result = self.m_components['color'][conf]

        return result

    def get_motion_sensor(self) :
        """ Return motion sensor
        ---
        returns (obj)   : The motion sensor
        """
        return self.m_hub.motion_sensor

    def get_light_matrix(self) :
        """ Return light matrix
        ---
        returns (obj)   : The light matrix
        """
        return self.m_hub.light_matrix

    def get_button(self, side) :
        """ Return hub button
        ---
        side (str)      : left or right, depending on the button to use
        ---
        returns (obj)   : The button
        """

        result = None

        if side == 'left' : result = self.m_hub.left_button
        elif side == 'right' : result = self.m_hub.right_button

        return result

    def get_wheels_distance(self) :
        """ Return the distance between the wheels in centimeters
        ---
        returns (float)   : The wheels distance in centimeters
        """
        return self.m_wheels_distance

    def get_wheel_diameter(self) :
        """ Return the wheel diameter in centimeters
        ---
        returns (float)   : The wheel diameter
        """
        return self.m_wheel_diameter

    def compute_distance(self, attachment, distance):
        """ Compute distance to give to robot so that it moves a given distance in the
        attachment direction
        ---
        attachment (str)    : name of the attachment in movement direction
        distance (str)      : distance to move the attachment
        ---
        returns (float)     : The distance according to the attachment position
        """
        result = distance

        if attachment in self.m_attachments :
            if self.m_attachments[attachment]['position'] == 'back' :
                result = - distance

        return result

    def get_attachment(self,name) :
        """ Return attachment
        ---
        name (str)      : Name of the attachment to get
        ---
        returns (obj)   : The attachment
        """

        result = None

        if name in self.m_attachments :
            result = self.m_attachments[name]
        else :
            self.log('Attachment ' + name + ' not found')

        return result

    def get_motor_from_attachment(self, attachment):
        """ Get the motor controlling the attachment
        ---
        name (str)      : Name of the attachment which motor shall be get
        ---
        returns (obj)   : The motor controlling the attachment
        """

        result = None

        if 'motor' in self.m_components :
            if attachment in self.m_attachments :
                if self.m_attachments[attachment]['position'] in self.m_components['motor'] :
                    result = self.m_components['motor'][self.m_attachments[attachment]['position']]
                else :
                    self.log('Motor ' + self.m_attachments[attachment]['position'] + \
                        ' for attachment ' + attachment + ' not found')
            else :
                self.log('Attachment ' + attachment + ' not found')
        else :
            self.log('No motor in robot')

        return result

    def measure(self) :
        """ Measure the robot state at a given time
        ---
        returns (dict) : The state of the robot at a given time
        """

        result = {}

        if 'motor' in self.m_components and 'left' in self.m_components['motor'] :
            result['left'] = self.m_components['motor']['left'].get_degrees_counted()
        if 'motor' in self.m_components and 'right' in self.m_components['motor'] :
            result['right'] = self.m_components['motor']['right'].get_degrees_counted()

        result['yaw'] = self.m_hub.motion_sensor.get_yaw_angle()
        result['roll'] = self.m_hub.motion_sensor.get_roll_angle()
        result['pitch'] = self.m_hub.motion_sensor.get_pitch_angle()

        return result
