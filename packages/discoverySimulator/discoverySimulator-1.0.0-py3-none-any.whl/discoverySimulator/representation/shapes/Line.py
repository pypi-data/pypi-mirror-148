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


from typing import List, Tuple

from PyQt5.QtCore import Qt, QLineF, QPointF
from PyQt5.QtGui import QPen, QPainter
from . import Shape, Rectangle
from .Point import Point


class Line(Shape):

    """ The Line class provides a line shape."""

    def __init__(self,length:float,width:float=1,color:str=None,opacity:int=255):
        """ Constructs a Line of the desired length, width and color.
        @param length  Length of the line [px]
        @param width  Width of the line [px]
        @param color  Color of the line [hex]
        @param opacity Opacity of the line (between 0 and 255)
        """
        super().__init__(color,opacity)
        self.__length=length
        self.__width=width

    # SETTERS
    def setLength(self,length:float):
        """ Changes the length of a line.
        @param length  Length of the line [px]"""
        self.__length=length

    # GETTERS
    @staticmethod
    def getLineCoefficient(line: QLineF) -> Tuple[float, float]:
        """ Returns the directing coefficient (m) and the y-intercept (p) of the QLineF (y = m.x + p)."""
        m = (line.y2() - line.y1()) / (line.x2() - line.x1())
        p = line.y1() - m * line.x1()
        return m, p

    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of the line."""
        return Rectangle(self.__width, self.__length)

    def contains(self, point:QPointF) -> bool:
        return False

    def getLineDecomposition(self) -> List[QLineF]:
        # Returns the QLineF decomposition of the line.
        x1 = self._pose.getX()
        y1 = self._pose.getY()
        dx = 0
        dy = self.__length
        x2,y2 = Point.computeTransformation(x1,y1,dx,dy,self._pose.getOrientation())

        return [QLineF(x1,y1,x2,y2)]

    def offset(self,value:float,truncated:bool=False) -> Rectangle:
        """ Returns the enlarged line shape of the selected offset.
        @param value  Offset size
        """
        rec = Rectangle(self.__width + 2 * value, self.__length + 2 * value)
        pose=self._pose.copy()
        dx,dy=Point.computeTransformation(pose.getX(), pose.getY(), 0, self.__length / 2, pose.getOrientation())
        pose.move(dx,dy)
        rec.setPose(pose)
        return rec

    def paint(self,painter:QPainter):
        # Draws the line in the graphic window.
        super().paint(painter)
        painter.setPen(QPen(self._color, self.__width, Qt.SolidLine))
        painter.drawLine(0, 0, 0, round(self.__length))