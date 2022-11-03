""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Class managing robust robot road following
# -------------------------------------------------------
# Color sensor shall be located between the 2 wheels
# -------------------------------------------------------
# Nadège LEMPERIERE, @10 october 2022
# Latest revision: 10 october 2022
# --------------------------------------------------- """

# Spike includes
from spike.control import wait_for_seconds

# Local includes
from commons.logger import ObjectWithLog

class RoadFollower(ObjectWithLog) :
    """ Class ensuring road following """

    m_line          = {}

    m_orienter      = None
    m_robot         = None

    def __init__(self, robot, logger, shall_trace, header) :
        """ Initialize road follower
        ---
        robot (obj)         : Robot model to use for road following
        logger (obj)        : Logger to use for logs collection
        shall_trace (bool)  : True if logs shall be collected
        header              : Trace header
        """

        super().__init__('RoadFollower', logger, shall_trace, header)

        self.log('Starting road follower creation')

        self.m_robot    = robot
        self.m_orienter = Path(robot, self.m_logger, shall_trace, header=header+'---')
        self.m_line     = {}

        self.log('Ending road_follower creation')

    def set_road(self, angle = 0, radius = 10, color = 'black') :
        """ Configure the current road to follow
        ---
        angle (float)       : Orientation of the line to look for (0 is vertical on the map)
        radius (float)      : Maximal distance in centimeters between the robot and the line
        color (str)         : Color of the line to look for
        """

        self.log('Starting road definition')

        self.m_line['angle']    = angle
        self.m_line['radius']   = radius
        self.m_line['color']    = color

        self.log('Ending road definition')

    def find_road(self) :
        """ Position the robot on the road
        ---
        return : True if the line has been found, False otherwise
        """

        self.log('Starting road search')
        found = False

        self.log('Position the robot orthogonally to the line','---')
        target_yaw = 90 + self.m_line['angle']
        self.m_orienter.set([
            {'yaw':target_yaw,  'distance':0.5,       'speed' : 100}
        ])
        self.m_orienter.move()

        self.log('Look for the road color in the given distance around the robot','---')

        found = self.find_color_in_direction(speed=10, step=0.05, color=self.m_line['color'])
        self.log('Line found','---')

        self.log('Ending road search')

        return found

    def follow_road(self) :
        """ Follow the road - once located on it """

        self.log('Starting following road')

        current_color = self.m_robot.get_color_sensor().get_color()
        while current_color is None : current_color = self.m_robot.get_color_sensor().get_color()
        self.log('Current color : ' + current_color,'---')

        shall_continue = current_color == self.m_line['color']
        if shall_continue : self.m_robot.get_motor('pair').start(steering=0, speed=-10)
        while shall_continue :
            current_color = self.m_robot.get_color_sensor().get_color()
            while current_color is None :
                current_color = self.m_robot.get_color_sensor().get_color()
            self.log('Current color : ' + current_color,'---')
            if current_color != self.m_line['color'] :
                self.m_robot.get_light_matrix().show_image('SAD')
                current_yaw = self.m_robot.get_motion_sensor().get_yaw_angle()
                self.log('Current yaw : ' + str(current_yaw),'---')
                if current_yaw != self.m_line['angle'] :
                    steering = int(10* (current_yaw - self.m_line['angle']) / \
                        abs(current_yaw - self.m_line['angle']))
                else :
                    steering = 0
                self.m_logger.log('Current steering : ' + str(steering),'---')
                self.m_robot.get_motor('pair').start_tank(\
                    left_speed=-steering, right_speed=steering)
                wait_for_seconds(0.1)

            else :
                self.m_robot.get_light_matrix().show_image('HAPPY')

        self.m_robot.get_motor('pair').stop()

        self.log('Ending following road')


    def find_color_in_direction(self, speed, step, color) :
        """ Look for the specified color along the robot direction, backwards and forwards, in a
        given distance range
        ---
        speed(float)        : Speed of the search
        step(float)         : Seconds between each color check
        color(str)          : Color to look for
        """

        local_speed = speed
        seconds = step
        iteration = 0
        shall_continue = True
        found = False
        while shall_continue :
            iteration += 1
            current_color = self.m_robot.get_color_sensor().get_color()
            while current_color is None :
                current_color = self.m_robot.get_color_sensor().get_color()
            self.log('Current color at iteration ' + str(iteration) + ' : ' + current_color,'---')
            if current_color == color :
                shall_continue = False
                found = True
            else :
                self.m_robot.get_motor('pair').start(speed = local_speed)
                wait_for_seconds(seconds)
                self.m_robot.get_motor('pair').stop()
                local_speed = -speed
                seconds += step
                if seconds > 5 : shall_continue = False

        self.m_robot.get_motor('pair').stop()

        return found
