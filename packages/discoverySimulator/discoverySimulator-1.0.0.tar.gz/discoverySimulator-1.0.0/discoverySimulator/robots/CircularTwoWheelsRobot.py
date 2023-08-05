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


from . import TwoWheelsRobot
from discoverySimulator.representation.shapes.Circle import Circle
from discoverySimulator.representation.Representation import Representation
import random

class CircularTwoWheelsRobot(TwoWheelsRobot):

    """ The CircularTwoWheelsRobot class provides a circular two wheels robot.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    def __init__(self, color:str=None, robotRadius:int=28, distanceBetweenWheels:int=50, wheelsRadius:int=10, wheelYPosition:int=0):
        """ Constructs a two wheels robot with a circular shape.
        @param color  Color of the robot [hex]
        @param robotRadius  Radius of the robot [px]
        @param distanceBetweenWheels  Distance between the wheels of the robot [px]
        @param wheelsRadius  Radius of the wheels [px]
        @param wheelYPosition  y-position of the wheels on the robot [px]"""
        color = random.choice(TwoWheelsRobot._COLORS) if color is None else color
        rep=Circle(robotRadius,color)
        rep.addOrientationMark()
        super().__init__(Representation(rep), distanceBetweenWheels, wheelsRadius, wheelYPosition)
