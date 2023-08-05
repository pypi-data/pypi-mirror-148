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


from PyQt5.QtGui import QColor

class Border:

    """ The Border class provides a border that can be added to a shape."""

    def __init__(self,width:int=0,color:str=None):
        """
        Constructs a border of the desired width and color that can be added to a shape.
        @param width Width of the border
        @param color  Color of the border
        """
        self.__width = int(width)
        self.__color = QColor(color)

    # GETTERS
    def getWidth(self) -> int:
        """ Returns the width of the border."""
        return self.__width

    def getColor(self) -> str:
        """ Returns the color of the border."""
        return self.__color