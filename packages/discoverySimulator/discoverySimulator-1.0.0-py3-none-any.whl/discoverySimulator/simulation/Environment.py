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


from PyQt5.QtCore import QSize
from discoverySimulator.Object import Object
from discoverySimulator.Observable import Observable
from discoverySimulator.Pose import Pose
from discoverySimulator.Frame import Frame
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line
from discoverySimulator.robots import Robot
from discoverySimulator.sensors import Sensor

from typing import List

class Environment(Observable):

    """ The Environment class provides an environment to simulate."""

    __DEFAULT_BORDER_SCREEN_WIDTH = 2

    # Available models : perfect, real (with noise)
    def __init__(self,width:int,height:int,model:str='perfect'):
        """ Constructs an environment which can be perfect or real.
        @param width  Width of the environment [px]
        @param height  Height of the environment [px]"""
        super().__init__()
        self.__objects=[]
        self.__virtualObjects=[]
        self.__sensors=[]

        self.__size = QSize(int(width),int(height))
        self.__frame=Frame(Pose(0, 0))

        self.__model=model

        self.__hasWalls=False
        self.__drawWalls()

    # GETTERS
    def getObjects(self) -> List[Object]:
        """ Returns all the objects added in the environment."""
        return self.__objects

    def getVirtualObjects(self) -> List[Object]:
        """ Returns all the virtuals objects added in the environment."""
        return self.__virtualObjects

    def getSensors(self) -> List[Sensor]:
        """ Returns all the sensors added in the environment and mounted on the robots present in the environment."""
        return self.__sensors

    def getFrame(self) -> Frame:
        # Returns the frame associated with the environnement (base frame).
        return self.__frame

    def getSize(self) -> QSize:
        """ Returns the size of the environment (QSize: .width() [px], .height() [px])."""
        return self.__size

    def getWidth(self) -> int:
        """ Returns the width of the environment [px]."""
        return self.__size.width()

    def getHeight(self) -> int:
        """ Returns the height of the environment [px]."""
        return self.__size.height()

    def hasWalls(self) -> bool:
        return self.__hasWalls

    def isReal(self):
        """ Returns True if the environment is real; otherwise returns False."""
        return self.__model=="real"

    def addObject(self, object:Object, x:float=0, y:float=0, orientation:float=0):
        """ Adds an object in the environment.
        @param object  Object of the class Object or which inherits from Object to add in the environment
        @param x  x-coordinate of the object in the environment [px]
        @param y  y-coordinate of the object in the environment [px]
        @param orientation  Orientation of the object in the environment [degrees]"""
        if isinstance(object, Object) and not object in self.__objects:
            pose=Pose(x,y,orientation)
            object.setPose(pose)
            object.setEnvironment(self)
            object.getFrame().setBaseFrame(self.__frame)
            object.getFrame().setCoordinates(pose)
            self.__objects.append(object)
            if isinstance(object, Robot):
                for comp in object.getComponents():
                    comp.setEnvironment(self)
                    if isinstance(comp, Sensor):
                        self.addSensor(comp)
                object.setOdometryPose(pose.copy())
            if isinstance(object, Sensor):
                self.addSensor(object)
            self.notifyObservers("objectCountChanged")

    def addVirtualObject(self, virtualObject:Object, x:float=0, y:float=0, orientation:float=0):
        """ Adds a virtual object in the environment.
        @param virtualObject  Object of the class Object or which inherits from Object to add in the environment
        @param x  x-coordinate of the object in the environment [px]
        @param y  y-coordinate of the object in the environment [px]
        @param orientation  Orientation of the object in the environment [degrees]"""
        if isinstance(virtualObject, Object) and not virtualObject in self.__virtualObjects:
            virtualObject.setPose(Pose(x, y, orientation))
            virtualObject.setEnvironment(self)
            self.__virtualObjects.append(virtualObject)

    def removeObject(self, object:Object):
        """ Removes an object of the environment.
        @param object  Object to remove"""
        if object in self.__objects:
            self.__objects.remove(object)
            if isinstance(object, Sensor):
                self.__sensors.remove(object)

    def removeVirtualObject(self, virtualObject:Object):
        """ Removes a virtual object of the environment.
        @param object  Virtual object to remove"""
        if virtualObject in self.__virtualObjects:
            self.__virtualObjects.remove(virtualObject)

    def addSensor(self,sensor:Sensor):
        if isinstance(sensor,Sensor) and not sensor in self.__sensors:
            self.__sensors.append(sensor)

    def __drawWalls(self):
        if not self.__hasWalls:
            self.addObject(Object(Representation(Line(self.__size.height(), Environment.__DEFAULT_BORDER_SCREEN_WIDTH, colors['tundora']))), 0, 0)
            self.addObject(Object(Representation(Line(self.__size.height(), Environment.__DEFAULT_BORDER_SCREEN_WIDTH, colors['tundora']))), self.__size.width(), 0)
            self.addObject(Object(Representation(Line(self.__size.width(), Environment.__DEFAULT_BORDER_SCREEN_WIDTH, colors['tundora']))), 0, 0, -90)
            self.addObject(Object(Representation(Line(self.__size.width(), Environment.__DEFAULT_BORDER_SCREEN_WIDTH, colors['tundora']))), 0, self.__size.height(), -90)
            self.__hasWalls=True