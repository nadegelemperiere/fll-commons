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
from math import pi, cos

# Local includes
from commons.pid import CorrectorPID
from commons.logger import ObjectWithLog

class Path(ObjectWithLog) :
    """ Class enabling robot base displacement (translation + rotation) """

    m_path                      = []
    m_parameters                = []

    m_robot                     = None
    m_pid                       = None

    s_default_rotation_speed    = 15

    def __init__(self, robot, logger, shall_trace = False,  header='---') :
        """ Initialize orienter
        ---
        robot (obj)         : Initialized robot
        logger (obj)        : Logger to use for log collection
        shall_trace (bool)  : True if traces shall be activated, false otherwise
        header              : Trace header
        """
        super().__init__('Path', logger, shall_trace, header)

        self.log('Starting PID filter creation')

        self.m_robot = robot
        self.m_path = []
        self.m_pid = CorrectorPID(1,0,0, True, self.m_logger, self.m_shall_trace)

        self.log('Ending PID filter creation')

    def set(self, path) :
        """ Set the path the robot shall follow
        ---
        path (array)        : List describing the sequence of movements.
        """

        self.m_path = []

        for movement in path :
            if 'distance' in movement :
                self.m_path.append(movement)
                if not 'yaw' in self.m_path[len(self.m_path) - 1] :
                    self.m_path[len(self.m_path) - 1]['yaw'] = 0
                if not 'speed' in self.m_path[len(self.m_path) - 1] :
                    self.m_path[len(self.m_path) - 1]['speed'] = 100
            else :
                self.log('Invalid path move :' + str(movement))


    def move(self, speed) :
        """ Move along the defined path
        ---
        This kind of movement is very precise, but very slow since it involves
        accelerating and deccelerating for every displacement step
        ---
        speed (float)        : Movement speed
        """

        motorpair = self.m_robot.get_motor('pair')
        if motorpair :

            for movement in self.m_path :
                self.__orient(
                    motorpair,
                    movement['yaw'],
                    speed = self.s_default_rotation_speed)
                motorpair.move(
                    movement['distance'],
                    speed=speed)

# pylint: disable=R0914
    def start(self, min_speed=20, ramp=0.2, max_speed = 100) :
        """ Launch controlled movement to follow path. This movement is
        less precise but more time efficient
        ---
        min_speed (float)   : Movement starting speed (0 to 100 - Should not be less than 20)
        max_speed (float)   : Movement maximal speed (0 to 100 - Should not be less than 20)
        ramp (float)        : Percentage of the displacement after which max speed shall be met
        and before which speed decrease shall start a the end of the movement to create the
        speed ramp
        """

        motorpair = self.m_robot.get_motor('pair')

        # Start the movement with minimal speed
        motorpair.start_at_power(min_speed,0)

        target_total_distance = 0
        current_total_distance = 0
        for movement in self.m_path :
            target_total_distance += abs(movement['distance'])

        self.log('Target distance : ' + str(target_total_distance))

        for movement in self.m_path :

            self.m_pid.initialize(movement['yaw'],0.1)
            shall_continue = True
            current_distance = 0

            previous_position = self.m_robot.measure()
            i_iteration = 0

            while shall_continue and i_iteration < 100:

                current_position = self.m_robot.measure()
                i_iteration += 1

                command_yaw = self.m_pid.update(current_position['yaw'])

                current_degrees = - 0.5 *(current_position['left'] - previous_position['left']) + \
                    0.5 * (current_position['right'] - previous_position['right'])
                # Distance is projected on the targeted path, to keep only the part of the
                # displacement which contributes to moving the robot in the right direction
                proj_distance = current_degrees / 360 * pi * self.m_robot.get_wheel_diameter() * \
                    cos((current_position['yaw'] - movement['yaw']) * 1.0 / 180 * pi)
                current_distance += proj_distance
                current_total_distance += proj_distance

                speed = self.__extrapolate_speed( \
                    movement['distance'], 0, current_distance, min_speed, ramp, max_speed)

                steering = 0
                if command_yaw != 0 :
                    steering = max(-100,min(100,int(50 * command_yaw / abs(command_yaw))))
                if movement['distance'] < 0 :
                    speed = -speed
                    steering = -steering

                self.log('Current robot measures : ' + str(current_position))
                self.log('Current distance in cm : ' + str(current_distance))
                self.log('Current total distance in cm : ' + str(current_total_distance))
                self.log('Speed : ' + str(speed))
                self.log('Steering : ' + str(steering))

                previous_position = current_position

                if abs(current_distance) >= abs(movement['distance']) and \
                    current_distance * movement['distance'] >= 0 : # Same sign
                    shall_continue = False
                else :
                    motorpair.start_at_power(int(speed),steering)

        motorpair.stop()
# pylint: enable=R0914

    def __orient(self, motorpair, yaw, speed = 100, iterations = 10) :
        """ Orient the robot in a given yaw angle without moving
        ---
        The center between the 2 wheels does not move during the process if no
        additional friction - does not work with additional wheels not motorized,
        consider the use of the small ball for stability
        ---
        motorpair(obj)      : Pair of motors to use for orientation
        yaw (float)         : Target yaw to reach in degrees
        iterations (int)    : Maximum allowed number of attempts
        speed (int)         : Orientation speed
        ---
        return (float)      : Reached yaw value
        """
        self.log('Starting orienter execution')
        self.log('Target yaw : ' + str(yaw))

        current_yaw = self.m_robot.get_motion_sensor().get_yaw_angle()
        iteration = 0
        self.log('Current yaw at iteration ' + str(iteration) + ' : ' + str(current_yaw))
        while abs(yaw - current_yaw) > 1 and iteration < iterations :
            iteration += 1
            self.__rotate(motorpair, yaw, current_yaw, speed)
            current_yaw = self.m_robot.get_motion_sensor().get_yaw_angle()
            self.log('Current yaw at iteration ' + str(iteration) + ' : ' + str(current_yaw))
            # In an ideal world, a single iteration would be enough, but friction can prevent the
            # target yaw angle to be reached, that's why additional iterations are sometimes useful

        self.log('Ending orienter execution')

    def __rotate(self, motorpair, target, current, speed = 100) :
        """ Rotate to go from current yaw to target yaw
        ---
        motorpair(obj)      : Pair of motors to use for orientation
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

        motorpair.move_tank(\
            distance, unit='cm', left_speed=left_speed, right_speed=right_speed)

# pylint: disable=R0913
    def __extrapolate_speed(self, target, initial, current, min_speed, ramp, max_speed) :
        """ Compute the speed according to the stage of the movement, following a trapezoid
        shape.
        ---
        target (float)  : Target distance after which movement is over
        initial (float) : Initial distance value
        current (float) : Current distance value
        min_speed (float)   : Movement starting speed (0 to 100 - Should not be less than 20)
        max_speed (float)   : Movement maximal speed (0 to 100 - Should not be less than 20)
        ramp (float)        : Percentage of the displacement after which max speed shall be met
        and before which speed decrease shall start a the end of the movement to create the
        """

        result = max_speed

        percentage = max(0,min(1,1.0 * (current - initial) / (target - initial)))
        self.log('Speed percentage : ' + str(percentage))
        self.log('Cur : ' + str(current) + ' Init : ' + str(initial) + ' Target : ' + str(target))
        if percentage < ramp :
            # Initial ramp for acceleration
            result = min_speed + percentage / ramp * (max_speed - min_speed)
        elif percentage > (1 - ramp) :
            # Final ramp for decceleration
            result = min_speed + (1 - percentage) / ramp * (max_speed - min_speed)

        return result
# pylint: enable=R0913
