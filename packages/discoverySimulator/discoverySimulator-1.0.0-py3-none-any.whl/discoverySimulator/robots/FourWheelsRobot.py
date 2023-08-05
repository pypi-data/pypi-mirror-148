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


from . import RectangularTwoWheelsRobot
from discoverySimulator.actuators.Wheel import Wheel
from discoverySimulator.config import *

class FourWheelsRobot(RectangularTwoWheelsRobot):

    """The FourWheelsRobot class provides a rectangular four wheels robot."""

    def __init__(self, color:str=None, width:int=50, height:int=60, distanceBetweenWheels:int=48, wheelsRadius:int=10, frontWheelYPosition:int=15, backWheelYPosition:int=-15):
        """ Constructs a four wheels robot with a rectangular shape.
        @param color  Color of the robot [hex]
        @param width  Width of the robot [px]
        @param height  Height of the robot [px]
        @param distanceBetweenWheels  Distances between the wheels of the robot [px]
        @param wheelsRadius  Radius of the wheels [px]
        @param frontWheelYPosition  y-position of the front wheels [px]
        @param backWheelYPosition  y-position of the back wheels [px]"""
        super().__init__(color, width, height, distanceBetweenWheels, wheelsRadius, frontWheelYPosition)
        self._backLeftWheel = Wheel(wheelsRadius, RectangularTwoWheelsRobot._DEFAULT_WHEEL_WIDTH)
        self._backRightWheel = Wheel(wheelsRadius, RectangularTwoWheelsRobot._DEFAULT_WHEEL_WIDTH)
        self.addComponent(self._backLeftWheel, (-distanceBetweenWheels + RectangularTwoWheelsRobot._DEFAULT_WHEEL_WIDTH) / 2, backWheelYPosition)
        self.addComponent(self._backRightWheel, (distanceBetweenWheels - RectangularTwoWheelsRobot._DEFAULT_WHEEL_WIDTH) / 2, backWheelYPosition)

        self._backLeftWheel.setID("BackLeftWheel")
        self._backRightWheel.setID("BackRightWheel")
        self._leftWheel.setID("FrontLeftWheel")
        self._rightWheel.setID("FrontRightWheel")

    # SETTERS
    def setFrontLeftWheelSpeed(self, speed: int):
        """ Sets the speed of the front left wheel.
        @param speed  Speed of the wheel [rpm]"""
        self.setLeftWheelSpeed(speed)

    def setFrontRightWheelSpeed(self, speed: int):
        """ Sets the speed of the front right wheel.
        @param speed  Speed of the wheel [rpm]"""
        self.setRightWheelSpeed(speed)

    def setBackLeftWheelSpeed(self, speed: int):
        """ Sets the speed of the back left wheel.
        @param speed  Speed of the wheel [rpm]"""
        if not self._isSpeedLocked:
            self._backLeftWheel.setSpeed(speed)

    def setBackRightWheelSpeed(self, speed: int):
        """ Sets the speed of the back right wheel.
        @param speed  Speed of the wheel [rpm]"""
        if not self._isSpeedLocked:
            self._backRightWheel.setSpeed(speed)

    def setBackWheelY(self, y: int):
        """ Sets the y-position of the back wheels.
        @param y  y-position of the wheels"""
        self._backRightWheel.getPose().setY(y)
        self._backLeftWheel.getPose().setY(y)

    # GETTERS
    def getFrontLeftWheel(self):
        """ Returns the front left wheel."""
        return self.getLeftWheel()

    def getFrontRightWheel(self):
        """ Returns the front right wheel."""
        return self.getRightWheel()

    def getBackLeftWheel(self):
        """ Returns the back left wheel."""
        return self._backLeftWheel

    def getBackRightWheel(self):
        """ Returns the back right wheel."""
        return self._backRightWheel

    def getRightLinearSpeed(self) -> float:
        """ Returns the right linear speed [px/min]."""
        return self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed()

    def getRightElementaryLinearSpeed(self) -> float:
        """ Returns the right elementary speed [px/timestep]."""
        return config["real_update_time_step"] / 60 * (
                    self._rightWheel.getRadius() * self._rightWheel.getSpeed() + self._backRightWheel.getRadius() * self._backRightWheel.getSpeed())

    def getLeftLinearSpeed(self) -> float:
        """ Returns the left linear speed [px/min]."""
        return self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed()

    def getLeftElementaryLinearSpeed(self) -> float:
        """ Returns the right elementary speed [px/timestep]."""
        return config["real_update_time_step"] / 60 * (self._leftWheel.getRadius() * self._leftWheel.getSpeed() + self._backLeftWheel.getRadius() * self._backLeftWheel.getSpeed())

    def computeRotationCenter(self):
        # Computes the rotation center of the robot according to the position of its wheels.
        self._pose.setRotationCenter((self._rightWheel.getPose().getX() + self._leftWheel.getPose().getX() + self._backRightWheel.getPose().getX() + self._backLeftWheel.getPose().getX()) / 4,(self._rightWheel.getPose().getY() + self._leftWheel.getPose().getY() + self._backRightWheel.getPose().getY() + self._backLeftWheel.getPose().getY()) / 4)



