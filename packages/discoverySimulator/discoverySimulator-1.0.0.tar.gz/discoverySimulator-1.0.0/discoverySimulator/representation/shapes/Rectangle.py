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
from typing import List

from PyQt5.QtCore import QRect, Qt, QLineF, QPointF
from PyQt5.QtGui import QPen, QBrush, QPainter
from . import Shape
from .Point import Point

class Rectangle(Shape):

    """ The Rectangle class provides a rectangle shape."""

    def __init__(self,width:float,height:float,color:str=None,borderRadius:float=0,opacity:int=255):
        """ Constructs a rectangle shape.
        @param width  Width of the rectangle [px]
        @param height  Height of the rectangle [px]
        @param color  Color of the rectangle [hex]
        @param borderRadius  BorderRadius of the rectangle [px]
        @param opacity  Opacity of the rectangle (between 0 and 255)"""
        super().__init__(color,opacity)
        self.__width=width
        self.__height=height
        self.__borderRadius=int(borderRadius)
        self._rect=QRect(-int(self.__width / 2), -int(self.__height / 2), int(self.__width), int(self.__height))

    # GETTERS
    def getWidth(self) -> float:
        """ Returns the width of the rectangle [px]."""
        return self.__width

    def getHeight(self) -> float:
        """ Returns the height of the rectangle [px]."""
        return self.__height

    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of the rectangle."""
        return self

    def getLineDecomposition(self) -> List[QLineF]:
        # Returns the QLineF decomposition of the rectangle.
        lines=[]
        w = self.__width / 2
        h = self.__height / 2
        sign = [(-1, -1), (-1, 1), (1, 1), (1, -1)] # Counterclockwise
        pts = []
        xo = self._pose.getX() + self._pose.getRotationCenterX()
        yo = self._pose.getY() + self._pose.getRotationCenterY()
        for i in range(4):
            x = self._pose.getX() + sign[i][0] * w
            y = self._pose.getY() + sign[i][1] * h
            dx = x - xo
            dy = y - yo
            pts.append(Point.computeTransformation(xo,yo,dx,dy,self._pose.getOrientation()))
        pts.append(pts[0])

        for i in range(4):
            lines.append(QLineF(pts[i][0],pts[i][1],pts[i+1][0],pts[i+1][1]))
        return lines

    def contains(self, point:QPointF) -> bool:
        # Returns True if the QPointF is inside the rectangle; otherwise returns False.
        for line in self.getLineDecomposition():
            d = (line.x2()-line.x1())*(point.y()-line.y1())-(line.y2()-line.y1())*(point.x()-line.x1())
            if not d<0: # Point to the right of the line (not good because trigonometric direction)
                return False
        return True

    def offset(self,value:float,truncated:bool=False) -> Rectangle:
        """ Returns the enlarged rectangle shape of the selected offset.
        @param value  Offset size, if positive, the circle is enlarged towards the outside, if negative, towards the inside
        """
        rectangle = Rectangle(self.__width + 2 * value, self.__height + 2 * value, self._color)
        rectangle.setPose(self._pose)
        return rectangle

    def paint(self,painter:QPainter):
        # Draws the rectangle in the graphic window.
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawRoundedRect(self._rect, self.__borderRadius, self.__borderRadius) # Draw from the center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter):
        # Draws the orientation mark of the rectangle in the graphic window.
        painter.setPen(QPen(self._color.lighter(Shape._ORIENTATION_MARK_LIGHTER_FACTOR), Shape._ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = Shape._ORIENTATION_MARK_WIDTH if self._border is None else max(Shape._ORIENTATION_MARK_WIDTH, self._border.getWidth())
        ypos = int(self.__height / 2 * 8 / 10)
        painter.drawLine(widthToCompensate - int(self.__width / 2), ypos, int(self.__width / 2) - widthToCompensate, ypos)