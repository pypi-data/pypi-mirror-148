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


from typing import Tuple, List

from PyQt5.QtCore import Qt, QLineF
from PyQt5.QtGui import QPen, QPainter
from discoverySimulator.representation.shapes import Shape, Rectangle
from math import radians, cos, sin


class Point(Shape):

    """ The Point class provides a point shape."""

    __POINT_SIZE = 5

    def __init__(self, color: str = "#000", opacity: int = 255):
        """ Constructs a point with the desired color.
        @param color  Color of the point [hex]
        @param opacity  Opacity of the point (between 0 and 255)
        """
        super().__init__(color, opacity)

    # GETTERS
    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of the point."""
        return Rectangle(self.__POINT_SIZE, self.__POINT_SIZE)

    def contains(self, point) -> bool:
        return False

    def getLineDecomposition(self) -> List[QLineF]:
        # Returns the QLineF decomposition of the point.
        return []

    @staticmethod
    def computeTransformation(xo: float, yo: float, dx: float, dy: float, o: float) -> Tuple[float, float]:
        """ Returns the coordinates of the point transformed with a rotation at a certain distance from the center of rotation.
        @param xo  x-coordinate of the center of rotation
        @param yo  y-coordinate of the center of rotation
        @param dx  x-offset distance from the center of rotation
        @param dy  y-offset distance from the center of rotation
        @param o  Angle of rotation [degrees]
        """
        a = -radians(o)
        return round(dx * cos(a) + dy * sin(a) + xo,3),round(-dx * sin(a) + dy * cos(a) + yo,3)

    def offset(self, value: float,truncated:bool=False) -> Rectangle:
        """ Returns the enlarged point shape of the selected offset.
        @param value  Offset size
        """
        rec = Rectangle(self.__POINT_SIZE + 2 * value, self.__POINT_SIZE + 2 * value)
        rec.setPose(self._pose.copy())
        return rec

    def paint(self, painter: QPainter):
        # Draws the point in the graphic window.
        super().paint(painter)
        painter.setPen(QPen(self._color, self.__POINT_SIZE, Qt.SolidLine))
        painter.drawPoint(0, 0)
