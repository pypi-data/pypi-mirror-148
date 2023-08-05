# discoverySimulator is a Python package allowing to simulate environments in which mobile robots evolve.
# This simulator is accompanied by an interface allowing to visualize and control the simulation.
# This package is ideal for a playful learning of python and a discovery of mobile robotics.
#
# Discovery Simulator - Copyright (C) 2022  Leo Planquette & Eloise Lefebvre
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.


from math import sqrt, sin, radians, cos, degrees, acos
from discoverySimulator.robots.Robot import Robot
from discoverySimulator.robots.TwoWheelsRobot import TwoWheelsRobot


class PathFollowing:

    """ The PathFollowing class provides a path following tool for a robot."""

    MAX_FORWARD_SPEED = 500
    MIN_FORWARD_SPEED = 300
    MIN_DISTANCE_FOR_MAX_FORWARD_SPEED = 60.0
    TURN_SPEED_FACTOR = 10
    DISTANCE_FOR_NEXT_POINT = 30
    DISTANCE_FOR_END_POINT = 5

    def __init__(self,robot):
        """ Constructs a following path tool.
        @param robot  Robot which will follow the path
        """
        if not isinstance(robot,TwoWheelsRobot):
            raise ValueError("To construct an instance of PathFollowing, an instance of TwoWheelsRobot has to be passed in parameter")

        self._robot = robot
        self._robot.setSpeedLock(True)
        self._path = None
        self._nextPointIndex = 0
        self._modifyOrientation = True

    # GETTERS
    def getRobot(self) -> Robot:
        """ Returns the robot which is following the path."""
        return self._robot

    def __angularDistance(self, pathPoint) -> float:
        # https://fr.wikihow.com/calculer-l%E2%80%99angle-entre-deux-vecteurs

        currentPosition=(self._robot.getPose().getX(),self._robot.getPose().getY())
        dx = pathPoint[0]-currentPosition[0]
        dy = pathPoint[1]-currentPosition[1]

        delta_degrees=2 # turn right
        v1 = (sin(-radians(self._robot.getPose().getOrientation())),cos(-radians(self._robot.getPose().getOrientation()))) # norm 1
        v1_delta = (sin(-radians(self._robot.getPose().getOrientation()+delta_degrees)),cos(-radians(self._robot.getPose().getOrientation()+delta_degrees)))
        v2=(dx,dy)

        dot_product = v1[0]*v2[0]+v1[1]*v2[1]
        dot_product_delta = v1_delta[0]*v2[0]+v1_delta[1]*v2[1]
        norm_v2=(v2[0]**2+v2[1]**2)**0.5

        theta = acos(dot_product/norm_v2)
        theta_delta = acos(dot_product_delta/norm_v2)

        return degrees(theta) * (-1 if degrees(theta)-degrees(theta_delta)>0 else 1)

    def startFollowing(self,path):
        """ Starts to following the path.
        @param path  Path to follow
        """
        if path is not None:
            self._path=path
            self._robot.setPathFollowing(self)

    def stopFollowing(self):
        self._path=None

    def followPath(self):
        """ Follows the path."""
        if self._path is not None:
            distance = sqrt((self._path[self._nextPointIndex][0]-self._robot.getPose().getX())**2+(self._path[self._nextPointIndex][1]-self._robot.getPose().getY())**2)
            angularDistance = self.__angularDistance(self._path[self._nextPointIndex])
            if (0<angularDistance<2 or 0>angularDistance>-2) and self._modifyOrientation:
                self._modifyOrientation=False

            f = min(PathFollowing.MIN_DISTANCE_FOR_MAX_FORWARD_SPEED,distance) / PathFollowing.MIN_DISTANCE_FOR_MAX_FORWARD_SPEED
            baseSpeed=max(PathFollowing.MAX_FORWARD_SPEED*f,PathFollowing.MIN_FORWARD_SPEED)/(abs(angularDistance)/(PathFollowing.TURN_SPEED_FACTOR if not self._modifyOrientation else 1)+1)
            self._robot.setSpeedLock(False)
            self._robot.setRightWheelSpeed(round(baseSpeed + PathFollowing.TURN_SPEED_FACTOR * angularDistance))
            self._robot.setLeftWheelSpeed(round(baseSpeed - PathFollowing.TURN_SPEED_FACTOR * angularDistance))
            self._robot.setSpeedLock(True)

            if (distance<PathFollowing.DISTANCE_FOR_NEXT_POINT and self._nextPointIndex<len(self._path)-1) \
                or (distance<PathFollowing.DISTANCE_FOR_END_POINT and self._nextPointIndex==len(self._path)-1):
                self._nextPointIndex+=1

            if self._nextPointIndex==len(self._path):
                self._robot.setSpeedLock(False)
                self._robot.setRightWheelSpeed(0)
                self._robot.setLeftWheelSpeed(0)
                self._robot.setPathFollowing(None)
