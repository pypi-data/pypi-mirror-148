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


from typing import List

from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter

from discoverySimulator.Pose import Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.Observable import Observable
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Border import Border

class Object(Observable):

    """ The Object class provides an object."""

    __number_of_instances = {}

    def __init__(self,representation):
        """ Constructs an object with the desired representation.
        @param representation  Representation of the object"""
        super().__init__()
        self._pose = None
        self._representation = representation
        self._environment= None
        self._isCollided = False
        self._isSelected = False
        self._visibilityLocked = False
        self._zIndex = 1
        self._frame=Frame()
        self._id = type(self).__name__.replace('Rectangular','').replace('Circular','')
        self.setNumberOfInstances(self._id)
        self.completeID()

    # SETTERS
    def setFrame(self,frame:Frame):
        """ Sets the frame associated with the object."""
        if isinstance(frame,Frame):
            self._frame=frame

    def setZIndex(self,index:int):
        """ Sets the z-index of the object.
        @param index  z-index of the object"""
        self._zIndex=int(index)

    def setNumberOfInstances(self,name:str):
        if name in self.__number_of_instances:
            Object.__number_of_instances[name]+=1
        else:
            Object.__number_of_instances[name]=1

    def setPose(self,pose:Pose):
        """ Sets the position of the object.
        @param  pose  Position of the object"""
        self._pose=pose
        self._representation.setPose(self._pose)

    def setVisible(self, visible:bool):
        """ Sets the visibility of the object.
        @param visible  Visibility of the object (True: the object will be displayed; False: the object will not be displayed)"""
        if not self._visibilityLocked:
            self._representation.setVisible(visible)
            self.visibilityChanged()

    def setVisibilityLocked(self,state:bool):
        self._visibilityLocked=state

    def setID(self,id:str):
        """ Sets the ID of the object.
        @param id  ID of the object"""
        Object.__number_of_instances[self._id.split("_")[0]] -= 1
        self._id=id
        self.setNumberOfInstances(self._id)
        self.completeID()

    def setSelected(self,selected:bool):
        if selected!=self._isSelected:
            self._isSelected=selected
            if self._isSelected:
                self._representation.getShape().addBorder(Border(4, "#31D5FF"))
            else:
                self._representation.getShape().removeBorder()
            self.notifyObservers("selectionChanged")

    def setCollidedState(self,state:bool):
        self._isCollided=state

    def setEnvironment(self, environment):
        self._environment=environment

    # GETTERS
    def getFrame(self) -> Frame:
        # Returns the frame associated with the object.
        return self._frame

    def getZIndex(self) -> int:
        """ Returns the z-index of the object."""
        return self._zIndex

    def getRepresentation(self) -> Representation:
        """ Returns the representation of the object."""
        return self._representation

    def getPose(self) -> Pose:
        """ Returns the position of the object."""
        return self._pose

    def getID(self) -> str:
        """ Returns the ID of the object."""
        return self._id

    def getVisibilityLocked(self) -> bool:
        return self._visibilityLocked

    def getEnvironment(self):
        """ Returns the environment of the object."""
        return self._environment

    def isCollided(self) -> bool:
        """ Returns True if the object is collided; otherwise returns False."""
        return self._isCollided

    def getIntersectionsWith(self,obj) -> List[QPointF]:
        return self.getRepresentation().getShape().getIntersectionsWith(obj.getRepresentation().getShape())

    def paint(self, painter:QPainter):
        # Draws the object in the graphic window.
        self._representation.paint(painter)

    def isVisible(self) -> bool:
        """ Returns True if the object is visible; otherwise returns False."""
        return self._representation.isVisible()

    def toggleVisible(self):
        """ Toggles the visibility of the object."""
        if not self._visibilityLocked:
            self._representation.toggleVisible()
            self.visibilityChanged()

    def visibilityChanged(self):
        self.notifyObservers("visibilityChanged")

    def completeID(self):
        self._id+="_"+str(Object.__number_of_instances[self._id])

    def isSelected(self) -> bool:
        return self._isSelected

    def computeCollisions(self):
        if not self._isCollided:
            for obj in self._environment.getObjects():
                if self!=obj and self._zIndex==obj.getZIndex() and self.isCollidedWith(obj):
                    self._isCollided=True
                    obj.setCollidedState(True)

    def isCollidedWith(self,obj) -> bool:
        """ Returns True if the object is collided with another object; otherwise returns False."""
        return len(self.getIntersectionsWith(obj))!=0