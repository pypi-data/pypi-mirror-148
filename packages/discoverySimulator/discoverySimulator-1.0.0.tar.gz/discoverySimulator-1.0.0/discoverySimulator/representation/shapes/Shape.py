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


from abc import ABC, abstractmethod
from typing import List

from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtGui import QColor, QPen, QPainter

from .Border import Border
from ...Pose import Pose


class Shape(ABC):
    """ The Shape class provides a shape mold."""

    _ORIENTATION_MARK_WIDTH = 2
    _ORIENTATION_MARK_LIGHTER_FACTOR = 160

    def __init__(self, color: str, opacity: int):
        """ Constructs a shape.
        @param color  Color of the shape [hex]
        @param opacity  Opacity of the shape (between 0 and 255)
        """
        self._color = QColor(color)
        self._opacity = opacity
        self._border = None
        self._pose = None
        self._orientationMark = False

    # SETTERS
    def setPose(self, pose: Pose):
        """ Sets the position of the shape.
        @param pose  Position of the shape
        """
        if isinstance(pose, Pose):
            self._pose = pose

    def setOpacity(self, opacity: int):
        """ Sets the opacity of the shape.
        @param opacity  Opacity of the shape (between 0 and 255)
        """
        self._opacity = opacity

    def setColor(self, color: str):
        """ Sets the color of the shape.
        @param color  Color of the shape [hex]
        """
        self._color = QColor(color)

    # GETTERS
    def getPose(self) -> Pose:
        """ Returns the position of the shape."""
        return self._pose

    def getColor(self) -> str:
        """ Returns the color of the shape."""
        return self._color.name()

    @abstractmethod
    def getLineDecomposition(self) -> List[QLineF]:
        # Returns the QLineF decomposition of the shape.
        pass

    def getIntersectionsWith(self, shape) -> List[QPointF]:
        # Returns all the intersections (QPointF) between the shape and another shape.

        # 3 possible cases due to the breakdown into lines:
        # -> circle vs circle
        # -> line vs line
        # -> circle vs line

        from .Point import Point
        if isinstance(self, Point) or isinstance(shape, Point):
            return []

        total_intersections = []
        shape1_lines = self.getLineDecomposition()
        shape2_lines = shape.getLineDecomposition()
        # Intersection circle/circle
        if not shape1_lines and not shape2_lines:
            total_intersections.extend(self.getIntersectionWithCircle(shape))
        # Intersection line/circle
        elif shape1_lines and not shape2_lines:
            for line in shape1_lines:
                intersections = shape.getIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)

        # Intersection circle/line
        elif not shape1_lines and shape2_lines:
            for line in shape2_lines:
                intersections = self.getIntersectionWithLine(line)
                if intersections:
                    total_intersections.extend(intersections)
        else:
            for r1_line in shape1_lines:
                for r2_line in shape2_lines:
                    intersection = QPointF()
                    if r1_line.intersect(r2_line, intersection) == QLineF.BoundedIntersection:
                        total_intersections.append(intersection)

        return total_intersections

    @abstractmethod
    def getBoundingBox(self):
        """ Returns the bounding box of the shape."""
        pass

    def addBorder(self, border: Border):
        """ Adds a border to the shape.
        @param border  Border to add
        """
        if isinstance(border, Border):
            self._border = border

    def removeBorder(self):
        """ Removes the border of the shape."""
        self._border = None

    @abstractmethod
    def contains(self, point):
        # Returns True if the QPointF is inside the shape; otherwise returns False.
        pass

    @abstractmethod
    def offset(self, value: float, truncated: bool = False):
        """ Returns the enlarged shape of the selected offset.
        @param value  Offset size, if positive, the shape is enlarged towards the outside, if negative, towards the inside
        """
        pass

    def addOrientationMark(self):
        """ Adds an orientation mark to the shape (works only for Rectangle and Circle)."""
        self._orientationMark = True

    def paint(self, painter: QPainter):
        # Draws the shape in the graphic window.
        painter.translate(self._pose.getX() + self._pose.getRotationCenterX(),
                          self._pose.getY() + self._pose.getRotationCenterY())
        painter.rotate(self._pose.getOrientation())
        painter.translate(-self._pose.getRotationCenterX(), -self._pose.getRotationCenterY())
        self._color.setAlpha(self._opacity)
        if self._border is not None:
            pen = QPen(self._border.getColor(), self._border.getWidth(), Qt.SolidLine)
            pen.setJoinStyle(Qt.RoundJoin)
            painter.setPen(pen)
        else:
            painter.setPen(Qt.NoPen)

    def paintOrientationMark(self, painter):
        # Draws the orientation mark of the shape in the graphic window.
        pass
