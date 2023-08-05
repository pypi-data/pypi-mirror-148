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

from PyQt5.QtCore import QPointF

from .shapes import Shape
from .. import Pose


class Representation:

    """ The Representation class provides the representation of an object."""

    def __init__(self,shape=None):
        """ Constructs a representation of an object.
        @param shape  Shape associated with the representation of the object
        """
        self.__shape=shape
        self.setShape(self.__shape)
        self.__subRepresentations=[]
        self.__pose=None
        self.__visible = True

    # SETTERS
    def setPose(self,pose:Pose):
        """ Sets the position of the representation."""
        self.__pose=pose
        self.__shape.setPose(self.__pose)

    def setShape(self,shape:Shape):
        """ Sets the shape associated with the representation."""
        if isinstance(shape,Shape):
            self.__shape=shape

    def setVisible(self,visible:bool):
        """ Sets the visibility of the representation."""
        self.__visible = visible

    # GETTERS
    def getShape(self) -> Shape:
        """ Returns the shape associated with the representation."""
        return self.__shape

    def addSubRepresentation(self, representation:Representation):
        """ Adds a sub-representation to the representation.
        @param representation  Sub-representation to add"""
        if isinstance(representation, Representation):
            self.__subRepresentations.append(representation)

    def toggleVisible(self):
        """ Toggles the visibility of the representation."""
        self.__visible=not self.__visible

    def isVisible(self) -> bool:
        """ Returns True is the representation is visible; otherwise returns False."""
        return self.__visible

    def paint(self,painter):
        # Draws the shape associated with the representation (if it is visible) in the graphic window. Then, draws all the sub-representations.
        if self.__visible:
            self.__shape.paint(painter)
            for rep in self.__subRepresentations:
                painter.save() # Save the state of the painter
                rep.paint(painter)
                painter.restore() # Restore the state of the painter

    def contains(self,point:QPointF) -> bool:
        # Returns True if the QPointF is inside the shape associated with the representation; otherwise returns False.
        return self.__shape.contains(point)
