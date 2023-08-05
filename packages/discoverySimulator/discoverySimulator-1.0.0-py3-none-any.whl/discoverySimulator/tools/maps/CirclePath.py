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


import random

from discoverySimulator import Object
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class CirclePath:

    """ The CirclePath class provides a circle path."""

    DEFAULT_WIDTH=20

    def  __init__(self, environment, color=colors['tundora']):
        """ Constructs a circle path in the given environment.
        @param environment  Environment where the circle path will be added
        @param color  Color of the circle path [hex]
        """
        self._environment = environment
        self._color = color
        self._pathElements = []

    def draw(self):
        """ Draws the circle path."""
        numberOfCircle=random.randint(1,2)
        if numberOfCircle==1:
            radius=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/2))
            circle1 = Object(Representation(Circle(radius,self._color)))
            circle2 = Object(Representation(Circle(radius-20,colors['gallery'])))
            self._environment.addVirtualObject(circle1,int(self._environment.getWidth()/2),int(self._environment.getHeight()/2))
            self._environment.addVirtualObject(circle2, int(self._environment.getWidth() / 2),int(self._environment.getHeight() / 2))
            self._pathElements.append(circle1)
            self._pathElements.append(circle2)
        else:
            radius1=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/4))
            radius2=random.randint(int(self._environment.getWidth()/8),int(self._environment.getWidth()/4))
            circle1 = Object(Representation(Circle(radius1, self._color)))
            circle2 = Object(Representation(Circle(radius1 - 20, colors['gallery'])))
            circle3 = Object(Representation(Circle(radius2,self._color)))
            circle4 = Object(Representation(Circle(radius2-20,colors['gallery'])))
            self._environment.addVirtualObject(circle1, int(self._environment.getWidth()/2)-radius1,int(self._environment.getHeight() / 2))
            self._environment.addVirtualObject(circle2, int(self._environment.getWidth()/2)-radius1,int(self._environment.getHeight() / 2))
            self._environment.addVirtualObject(circle3, int(self._environment.getWidth()/2)-20+radius2,int(self._environment.getHeight() / 2))
            self._environment.addVirtualObject(circle4, int(self._environment.getWidth()/2)-20+radius2,int(self._environment.getHeight() / 2))
            self._pathElements.append(circle1)
            self._pathElements.append(circle2)
            self._pathElements.append(circle2)
            self._pathElements.append(circle3)

    def delete(self):
        """ Deletes all the elements of the path."""
        for item in self._pathElements:
            self._environment.removeVirtualObject(item)
        self._pathElements.clear()





