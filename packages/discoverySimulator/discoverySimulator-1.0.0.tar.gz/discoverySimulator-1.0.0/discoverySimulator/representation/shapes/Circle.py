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

from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QBrush, QPen
from PyQt5.QtGui import QPainter
from . import Shape, Rectangle
from .Line import Line


class Circle(Shape):

    """ The Circle class provides a circle shape."""

    def __init__(self,radius:float,color:str,opacity:int=255):
        """ Constructs a circle shape.
        @param radius  Radius of the circle [px]
        @param color  Color of the circle [hex]
        @param opacity  Opacity of the circle (between 0 and 255)"""
        super().__init__(color,opacity)
        self.__radius=radius

    # GETTERS
    def getRadius(self) -> float :
        """ Returns the radius of the circle [px]."""
        return self.__radius

    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of the circle."""
        return Rectangle(self.__radius * 2, self.__radius * 2)

    def contains(self, point:QPointF) -> bool:
        # Returns True if the QPointF is inside the circle; otherwise returns False.
        return (point.x()-self._pose.getX()) ** 2 + (point.y()-self._pose.getY()) ** 2 <= self.__radius ** 2

    def getLineDecomposition(self) -> List[QLineF]:
        # Returns the QLineF decomposition of the circle.
        return []

    def getIntersectionWithLine(self,line:QLineF) -> List[QPointF]:
        # Returns all the intersections (QPointF) between the circle and a QLineF.
        intersections = []
        if line.x2()!=line.x1(): # Not a vertical line
            a_line,b_line=Line.getLineCoefficient(line)

            A = 1+a_line**2
            B = -2*self._pose.getX()+2*a_line*(b_line-self._pose.getY())
            C = self._pose.getX() ** 2 + (b_line-self._pose.getY()) ** 2 - self.__radius ** 2

            delta = B**2-4*A*C
            if delta>=0:
                max_x = line.x2() if line.x2() > line.x1() else line.x1()
                min_x = line.x2() if line.x2() < line.x1() else line.x1()

                x1=(-B-delta**0.5)/(2*A)
                x2=(-B+delta**0.5)/(2*A)
                # x1 = x2 if the line is tangent to the circle
                y1=a_line*x1+b_line
                y2 = a_line * x2 + b_line

                if min_x<=x1<=max_x:
                    intersections.append(QPointF(x1,y1))
                if min_x<=x2<=max_x: # The point belongs to the segment
                    intersections.append(QPointF(x2, y2))
        else: # Vertical line
            A=1
            B=-2*self.getPose().getY()
            C= self.getPose().getY() ** 2 + (line.x1()-self.getPose().getX()) ** 2 - self.__radius ** 2

            delta = B**2-4*A*C
            if delta>=0:
                max_y = line.y2() if line.y2() > line.y1() else line.y1()
                min_y = line.y2() if line.y2() < line.y1() else line.y1()

                y1 = (-B-delta**0.5)/(2*A)
                y2 = (-B+delta**0.5)/(2*A)
                if y1 >= min_y and y1 <= max_y:
                    intersections.append(QPointF(line.x1(),y1))
                if y2 >= min_y and y2 <= max_y:  # The point belongs to the segment
                    intersections.append(QPointF(line.x1(),y2))
        return intersections

    def getIntersectionWithCircle(self, circle) -> List[QPointF]:
        # Returns all the intersections (QPointF) between the circle and another circle.
        # https://fr.planetcalc.com/8098/
        intersections=[]

        d=((self._pose.getX()-circle.getPose().getX())**2 + (self._pose.getY()-circle.getPose().getY())**2)**0.5
        if d>self.__radius+circle.getRadius() or d<abs(self.__radius - circle.getRadius()) or d==0:
            return intersections

        a= (self.__radius ** 2 - circle.getRadius() ** 2 + d ** 2) / (2 * d)
        h= (self.__radius ** 2 - a ** 2) ** 0.5
        p1=QPointF(self._pose.getX(),self._pose.getY())
        p2=QPointF(circle.getPose().getX(),circle.getPose().getY())
        p3=p1+a/d*(p2-p1)

        hd=h/d
        dx=p2.x()-p1.x()
        dy=p2.y()-p1.y()

        intersections.append(QPointF(p3.x()+hd*dy,p3.y()-hd*dx))
        intersections.append(QPointF(p3.x()-hd*dy,p3.y()+hd*dx))
        return intersections

    def offset(self,value:float,truncated:bool=False) -> Circle:
        """ Returns the enlarged circle shape of the selected offset.
        @param value  Offset size, if positive, the circle is enlarged towards the outside, if negative, towards the inside
        """
        circle = Circle(self.__radius + value, self._color)
        circle.setPose(self._pose)
        return circle

    def paint(self,painter:QPainter):
        # Draws the circle in the graphic window.
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawEllipse(-self.__radius, -self.__radius, self.__radius * 2, self.__radius * 2) # Draw from the center
        if self._orientationMark:
            self.paintOrientationMark(painter)

    def paintOrientationMark(self,painter:QPainter):
        # Draws the orientation mark of the circle in the graphic window.
        painter.setPen(QPen(self._color.lighter(Shape._ORIENTATION_MARK_LIGHTER_FACTOR), Shape._ORIENTATION_MARK_WIDTH, Qt.SolidLine))
        widthToCompensate = Shape._ORIENTATION_MARK_WIDTH if self._border is None else max(Shape._ORIENTATION_MARK_WIDTH, self._border.getWidth())
        ypos = int(self.__radius * 8 / 10)
        painter.drawLine(widthToCompensate - int(self.__radius / 2), ypos, int(self.__radius / 2) - widthToCompensate, ypos)