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


from discoverySimulator.Pose import Pose
from discoverySimulator.representation.shapes import Point

class Frame:

    """ The Frame class provides a Frame."""

    def __init__(self,coordinates=None,baseFrame=None):
        self.__coordinates=None
        self.__baseFrame=None
        self.setCoordinates(coordinates)
        self.setBaseFrame(baseFrame)

    # SETTERS
    def setCoordinates(self,coordinates):
        """ Sets the position of the object in the current marker."""
        if isinstance(coordinates,Pose):
            self.__coordinates=coordinates

    def setBaseFrame(self,baseFrame):
        """ Sets the reference frame for the object."""
        if isinstance(baseFrame,Frame):
            self.__baseFrame = baseFrame

    # GETTERS
    def getBaseFrame(self):
        """ Returns the reference frame for the object."""
        return self.__baseFrame

    def getCoordinates(self):
        """ Returns the position of the object in the current marker."""
        return self.__coordinates

    def getAbsoluteCoordinates(self):
        """ Returns the position of the object in the base frame (environment marker)."""
        if self.__baseFrame is not None:
            absBf = self.__baseFrame.getAbsoluteCoordinates()
            bfX = absBf.getX()
            bfY = absBf.getY()

            dx = self.__coordinates.getX()
            dy = self.__coordinates.getY()

            X, Y = Point.computeTransformation(bfX, bfY, dx, dy, absBf.getOrientation())

            abs=Pose(X,Y,absBf.getOrientation()+self.__coordinates.getOrientation())
            del absBf
            return abs
        else:
            return self.__coordinates.copy()