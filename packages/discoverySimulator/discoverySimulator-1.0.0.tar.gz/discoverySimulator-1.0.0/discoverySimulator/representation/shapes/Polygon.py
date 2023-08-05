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
from typing import List, Tuple

from PyQt5.QtCore import Qt, QLineF, QPoint, QPointF
from PyQt5.QtGui import QPolygon, QBrush, QPainter

from discoverySimulator.Pose import Pose
from discoverySimulator.representation.shapes import Shape, Rectangle

class Polygon(Shape):

    """ The Polygon class provides a polygon shape."""

    def __init__(self,points:List[Tuple[int,int]],color:str=None,clockwise:bool=True,opacity:int=255):
        """ Constructs a polygon shape.
        @param points  Points that determine the shape of the polygon
        @param color  Color of the polygon [hex]
        @param clockwise Determine the drawing direction of the polygon points
        @param opacity  Opacity of the polygon (between 0 and 255)"""
        super().__init__(color,opacity)
        self.__points=[QPoint(round(point[0]),round(point[1])) for point in points]
        self.__clockwise=clockwise

    # GETTERS
    def getBoundingBox(self) -> Rectangle:
        """ Returns the bounding box of the polygon."""
        min_x=self.__points[0].x()
        min_y = self.__points[0].y()
        max_x=self.__points[0].x()
        max_y = self.__points[0].y()

        for point in self.__points:
            if point.x()<min_x:
                min_x=point.x()
            if point.y()<min_y:
                min_y = point.y()
            if point.x()>max_x:
                max_x = point.x()
            if point.y()>max_y:
                max_y=point.y()
        return Rectangle(max_x-min_x,max_y-min_y)

    def setPose(self,pose:Pose):
        # Overloaded method
        # Modifies the pose of the polygon so that the new pose is the average of all points.
        sx=0
        sy=0
        for point in self.__points:
            sx+=point.x()+pose.getX()
            sy+=point.y()+pose.getY()
        sx=round(sx/len(self.__points))
        sy=round(sy/len(self.__points))

        for point in self.__points:
            point.setX(point.x()+pose.getX()-sx)
            point.setY(point.y()+pose.getY()-sy)

        pose.setX(sx)
        pose.setY(sy)
        self._pose=pose

    def contains(self, point) -> bool:
        # Returns True if the QPointF is inside the polygon; otherwise returns False.
        # https://wrf.ecse.rpi.edu/Research/Short_Notes/pnpoly.html
        pose = QPoint(self._pose.getX(), self._pose.getY())
        c=False
        j= len(self.__points) - 1
        for i in range(len(self.__points)):
            previousEdge= self.__points[j] + pose
            edge = self.__points[i] + pose
            if ((edge.y() > point.y()) != (previousEdge.y() > point.y())) and (point.x() < (previousEdge.x() - edge.x()) * (point.y() - edge.y()) / (previousEdge.y() - edge.y()) + edge.x()):
                c=not c
            j=i
        return c

    def getLineDecomposition(self) -> List[QLineF]:
        # Returns the QLineF decomposition of the polygon.
        lines=[]
        pose = QPoint(self._pose.getX(),self._pose.getY())
        points_number=len(self.__points)
        for i in range (1,points_number+1):
            lines.append(QLineF(self.__points[i - 1] + pose, self.__points[i if i < points_number else 0] + pose))
        return lines

    def offset(self,value:float,truncated:bool=False) -> Polygon:
        """ Returns the enlarged polygon shape of the selected offset.
        @param value  Offset size, if positive, the polygon is enlarged towards the outside, if negative, towards the inside
        @param truncated  This value can be set to True if the polygon must be truncated
        """
        # https://stackoverflow.com/questions/54033808/how-to-offset-polygon-edges
        points_offset=[]
        truncated_points_offset=[]
        points_number=len(self.__points)
        truncLines=[]

        value *= (1 if self.__clockwise else -1)
        for curr in range(points_number):
            prev = (curr + points_number - 1) % points_number
            next = (curr + 1) % points_number

            line1 = QLineF(self.__points[prev].x(), self.__points[prev].y(), self.__points[curr].x(), self.__points[curr].y())
            line2 = QLineF(self.__points[curr].x(), self.__points[curr].y(), self.__points[next].x(), self.__points[next].y())
            line1_normal=line1.normalVector()
            line2_normal=line2.normalVector()

            na = QPointF(line1_normal.x2()-line1_normal.x1(),line1_normal.y2()-line1_normal.y1())
            na/=line1_normal.length()

            nb = QPointF(line2_normal.x2()-line2_normal.x1(),line2_normal.y2()-line2_normal.y1())
            nb/=line2_normal.length()

            bis=na+nb
            length_bis = (bis.x()**2+bis.y()**2)**0.5
            bis/=length_bis

            l=value/(1+na.x()*nb.x()+na.y()*nb.y())**0.5

            p_prime = self.__points[curr] + 2**0.5 * l * bis
            points_offset.append((p_prime.x(),p_prime.y()))

            if truncated:
                if abs(l)>abs(value):
                    t=self.__points[curr] + value * bis
                    truncLines.append(QLineF(t.x(),t.y(),self.__points[curr].x(),self.__points[curr].y()).normalVector())
                else:
                    truncLines.append(None)

        if truncated:
            for curr in range(points_number):
                if truncLines[curr] is not None:
                    prev = (curr + points_number - 1) % points_number
                    next = (curr + 1) % points_number

                    lines=[QLineF(points_offset[prev][0],points_offset[prev][1],points_offset[curr][0],points_offset[curr][1]),
                           QLineF(points_offset[curr][0], points_offset[curr][1], points_offset[next][0],points_offset[next][1])]

                    for line in lines:
                        intersection = QPointF()
                        if line.intersect(truncLines[curr],intersection)==QLineF.UnboundedIntersection or line.intersect(truncLines[curr],intersection)==QLineF.BoundedIntersection:
                            truncated_points_offset.append((intersection.x(),intersection.y()))
                else:
                    truncated_points_offset.append(points_offset[curr])
            points_offset=truncated_points_offset
        pol=Polygon(points_offset)
        pol.setPose(self._pose.copy())
        return pol

    def paint(self, painter:QPainter):
        # Draws the polygon in the graphic window.
        super().paint(painter)
        painter.setBrush(QBrush(self._color, Qt.SolidPattern))
        painter.drawPolygon(QPolygon(self.__points))



