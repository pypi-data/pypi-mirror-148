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


from math import cos,sin,radians,degrees

from discoverySimulator.config import config
from . import Robot
from discoverySimulator.actuators.Wheel import Wheel

class TwoWheelsRobot(Robot):

    """ The TwoWheelsRobot class provides a two wheels robot with a configurable shape."""

    _DEFAULT_WHEEL_WIDTH = 8
    _COLORS = ["#fdcb6e", "#00cec9", "#55efc4", "#a29bfe"]

    def __init__(self, representation, distanceBetweenWheels:float, wheelsRadius:float, wheelYPosition:float):
        """ Create a two wheels robot with the desired representation and wheels parameters.
        @param representation  Representation of the robot
        @param distanceBetweenWheels  Distance between the wheels of the robot [px]
        @param wheelsRadius  Radius of the wheels [px]
        @param wheelYPosition  y-position of the wheels on the robot [px]"""
        super().__init__(representation)
        self._leftWheel = Wheel(wheelsRadius, self._DEFAULT_WHEEL_WIDTH)
        self._rightWheel = Wheel(wheelsRadius, self._DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._leftWheel, (-distanceBetweenWheels + self._DEFAULT_WHEEL_WIDTH) / 2, wheelYPosition)
        self.addComponent(self._rightWheel, (distanceBetweenWheels - self._DEFAULT_WHEEL_WIDTH) / 2, wheelYPosition)
        self._distanceBetweenWheels = distanceBetweenWheels
        self._leftWheel.setID("LeftWheel")
        self._rightWheel.setID("RightWheel")

    # SETTERS
    def setLeftWheelSpeed(self,speed:int):
        """ Sets the speed of the left wheel.
        @param speed  Speed of the wheel [rpm]"""
        if not self._isSpeedLocked:
            self._leftWheel.setSpeed(speed)

    def setRightWheelSpeed(self,speed:int):
        """ Sets the speed of the right wheel.
        @param speed  Speed of the wheel [rpm]"""
        if not self._isSpeedLocked:
            self._rightWheel.setSpeed(speed)

    # GETTERS
    def getAverageSpeed(self):
        """ Returns the average speed of the robot [px/timestep]."""
        averageSpeedRobot = (self.getRightElementaryLinearSpeed() + self.getLeftElementaryLinearSpeed()) / 2
        return averageSpeedRobot

    def getRightWheel(self) -> Wheel:
        """ Returns the speed of the right wheel [rpm]."""
        return self._rightWheel

    def getLeftWheel(self) -> Wheel:
        """ Returns the speed of the left wheel [rpm]."""
        return self._leftWheel

    def getRightLinearSpeed(self) -> float:
        """ Returns the right wheel linear speed [px/min]."""
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed()

    def getRightElementaryLinearSpeed(self) -> float:
        """ Returns the elementary speed of the right wheel [px/timestep]."""
        return self.getRightLinearSpeed()*config["real_update_time_step"] / 60

    def getLeftLinearSpeed(self) -> float:
        """ Returns the left wheel linear speed [px/min]."""
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed()

    def getLeftElementaryLinearSpeed(self) -> float:
        """ Returns the elementary speed of the left wheel [px/timestep]."""
        return self.getLeftLinearSpeed() * config["real_update_time_step"] / 60

    def getDistanceBetweenWheels(self) -> float:
        """ Returns the distance between the wheels of the robot [px]."""
        return self._distanceBetweenWheels

    def move(self):
        # Calculates the displacement of the robot according to the parameters of its wheels.
        if not self._isCollided:
            # Average speed of the robot
            averageSpeedRobot = (self.getRightElementaryLinearSpeed() + self.getLeftElementaryLinearSpeed()) / 2

            # Speed along the x and y axes
            Phi = radians(self._pose.getOrientation() + 90)
            dx = averageSpeedRobot * cos(Phi)
            dy = averageSpeedRobot * sin(Phi)

            # Angular speed
            dPhi = -degrees((self.getRightElementaryLinearSpeed() - self.getLeftElementaryLinearSpeed()) / (2 * self._distanceBetweenWheels)) # indirect benchmark so minus sign

            self._pose.move(self._pose.getX() + dx, self._pose.getY() + dy)
            self._pose.rotate(dPhi)

            self.computeCollisions()
        super().move()

    def computeRotationCenter(self):
        # Computes the rotation center of the robot according to the position of its wheels.
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX()) / 2,
                                         (self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY()) / 2)



