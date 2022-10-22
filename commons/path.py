""" -----------------------------------------------------
# Copyright (c) [2022] Nadege LEMPERIERE
# All rights reserved
# -------------------------------------------------------
# Class managing robust robot orientation
# -------------------------------------------------------
# Nadège LEMPERIERE, @10 october 2022
# Latest revision: 10 october 2022
# --------------------------------------------------- """

# System includes
from math import pi

class Path :
    """ Class enabling robot base displacement (translation + rotation) """

    m_shall_trace   = False
    m_trace_header  = ''

    m_path          = []
    m_parameters    = []

    m_robot         = None

    def __init__(self, robot, shall_trace = False,  header='---') :
        """ Initialize orienter
        ---
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        robot (obj)         : Initialized robot
        th                  : Trace header
        """
        self.m_shall_trace = shall_trace
        self.m_trace_header = header

        if self.m_shall_trace : print(self.m_trace_header + ' Starting orienter creation')

        self.m_robot = robot
        self.m_path = []

        if self.m_shall_trace : print(self.m_trace_header + ' Ending orienter creation')

    def set(self, path) :
        """ Set the path the robot shall follow
        ---
        path (array)        : List describing the sequence of movements.
        """

        self.m_path = []

        for action in path :
            if action['type'] == 'move' and 'distance' in action :
                self.m_path.append(action)
                if not 'speed' in self.m_path[len(self.m_path) - 1] :
                    self.m_path[len(self.m_path) - 1]['speed'] = 100
            elif action['type'] == 'orient' and 'angle' in action :
                while action['angle'] < -180 : action['angle'] += 360
                while action['angle'] > 180 : action['angle'] -= 360
                self.m_path.append(action)
                if not 'speed' in self.m_path[len(self.m_path) - 1] :
                    self.m_path[len(self.m_path) - 1]['speed'] = 100
            elif self.m_shall_trace :
                print(self.m_trace_header + 'Invalid path move :' + str(action))


    def follow(self) :
        """ Follow the defined path
        """

        for action in self.m_path :
            if action['type'] == 'move' :
                self.m_robot.get_motor('pair').move(
                    self.m_robot.compute_distance(action['distance']),
                    speed=action['speed'])
            elif action['type'] == 'orient' :
                self.__orient(
                    action['angle'],
                    speed=action['speed'])

    def __orient(self, yaw, speed = 100, iterations = 10) :
        """ Orient the robot in a given yaw angle
        ---
        The center between the 2 wheels does not move during the process if no
        additional friction - does not work with additional wheels not motorized,
        consider the use of the small ball for stability
        ---
        yaw (float)         : Target yaw to reach in degrees
        iterations (int)    : Maximum allowed number of attempts
        speed (int)         : Orientation speed
        ---
        return (float)      : Reached yaw value
        """

        if self.m_shall_trace : print(self.m_trace_header + ' Starting orienter execution')
        if self.m_shall_trace : print(self.m_trace_header + '--- Target yaw : ' + str(yaw))

        current_yaw = self.m_robot.get_motion_sensor().get_yaw_angle()
        iteration = 0
        if self.m_shall_trace : print(self.m_trace_header + \
            '--- Current yaw at iteration ' + str(iteration) + ' : ' + str(current_yaw))
        while abs(yaw - current_yaw) > 1 and iteration < iterations :
            iteration += 1
            self.__rotate(yaw, current_yaw, speed)
            current_yaw = self.m_robot.get_motion_sensor().get_yaw_angle()
            if self.m_shall_trace : print(self.m_trace_header + \
                '--- Current yaw at iteration ' + str(iteration) + ' : ' + str(current_yaw))
            # In an ideal world, a single iteration would be enough, but friction can prevent the
            # target yaw angle to be reached, that's why additional iterations are sometimes useful

        if self.m_shall_trace : print('--- Ending orienter execution')

    def __rotate(self, target, current, speed = 100) :
        """ Rotate to go from current yaw to target yaw
        ---
        target (float)      : Target yaw to reach in degrees
        current (float)     : Current yaw in degrees
        speed (int)         : Rotation speed
        """

        # When setting steering to a maximal value, one of the first wheel does not move, and the
        # second rotates on the circle O, which center is the first wheel, and which radius is the
        # distance between the wheels. If the travelled distance is set to the perimeter of the
        # circle O, then the robot will undergo a 360 degrees rotation.
        # To achieve a smaller rotation, the distance shall be set to the corresponding portion of
        # the circle O perimeter.
        delta = current - target
        while delta < -180 : delta += 360
        while delta > 180 : delta -= 360

        distance = abs(delta) / 360 * 2 * pi * self.m_robot.get_wheels_distance() / 2

        # The direction shall be set to -100 or 100 (maximal values) depending on the rotation
        # direction, which is linked to the sign of the diff between target yaw and current yaw
        if delta < 0 :
            left_speed = speed
            right_speed = -speed
        elif delta > 0 :
            left_speed = -speed
            right_speed = speed
        else :
            left_speed = 0
            right_speed = 0

        self.m_robot.get_motor('pair').move_tank(\
            distance, unit='cm', left_speed=left_speed, right_speed=right_speed)
