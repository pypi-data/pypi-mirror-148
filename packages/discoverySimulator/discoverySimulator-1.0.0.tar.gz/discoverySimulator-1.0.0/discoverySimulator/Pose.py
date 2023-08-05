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


from __future__ import annotations

class Pose:

    """ The Pose class provides a position representation with a coordinates system and an orientation associated with an object."""

    def __init__(self, x:float, y:float,orientation:float=0,rx:float=0,ry:float=0):
        """ Constructs a pose for an object.
        @param x  x coordinate [px]
        @param y  y coordinate [px]
        @param orientation  Orientation [degrees]
        @param rx  x rotation center [px]
        @param ry  y rotation center [px]
        """
        self.__pose = [x, y]
        self.setRotationCenter(rx, ry)
        self.__orientation = orientation

    # SETTERS
    def setX(self,x:float):
        """ Sets the x coordinate of the object in its base frame.
        @param x  x coordinate [px]"""
        self.__pose[0]=x

    def setY(self,y:float):
        """ Sets the y coordinate of the object in its base frame.
        @param y  y coordinate [px]"""
        self.__pose[1]=y

    def setOrientation(self, orientation:float):
        """ Sets the orientation of the object in its base frame.
        @param orientation  Orientation [degrees]"""
        self.__orientation=orientation

    def setRotationCenter(self, rx:float, ry:float):
        """ Sets the x rotation center coordinate of the object in the environment.
        @param rx  x rotation center coordinate [px]"""
        self.__rotationCenter=(rx, ry)

    # GETTERS
    def getX(self) -> float:
        """ Returns the x coordinate of the object in its base frame [px]."""
        return self.__pose[0]

    def getY(self) -> float:
        """ Returns the y coordinate of the object in its base frame [px]."""
        return self.__pose[1]

    def getRotationCenterX(self) -> float:
        """ Returns the x rotation center coordinate of the object in its base frame [px]."""
        return self.__rotationCenter[0]

    def getRotationCenterY(self) -> float:
        """ Returns the y rotation center coordinate of the object in its base frame [px]."""
        return self.__rotationCenter[1]

    def getOrientation(self) -> float:
        """ Returns the orientation of the object in its base frame [degrees]."""
        return self.__orientation

    def move(self,x:float,y:float):
        """ Moves the position of the object in its base frame."""
        self.__pose=[x, y]

    def rotate(self, angle:float):
        """ Rotates the object in its base frame.
        @param angle  Variation of orientation [degrees]
        """
        self.__orientation = (self.__orientation + angle) % 360

    def copy(self) -> Pose:
        """ Returns a copy of the Pose of the object."""
        return Pose(self.__pose[0], self.__pose[1], self.__orientation, self.__rotationCenter[0], self.__rotationCenter[1])