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


import random
from abc import ABC,abstractmethod
from typing import List
from math import cos, sin, radians, degrees, atan


from .. import Object
from ..Component import Component
from ..actuators import Wheel
from ..representation.Representation import Representation
from ..representation.shapes.Point import Point
from ..config import *
from ..Pose import Pose
from ..sensors import Sensor


class Robot(ABC,Object):

    """ The Robot class provides a mold to implement robots."""

    __NUMBER_CALLS_BEFORE_REFRESH = 30
    __MAX_POINTS_NUMBER_IN_ARRAY = 50

    def __init__(self,representation):
        """ Constructs a robot with the desired representation.
        @param representation  Representation of the robot
        """
        super().__init__(representation)
        self._components=[]
        self._sensors_counter=0
        self._actuators_counter=0
        self._wheels=[]

        # TRAJECTORY ATTRIBUTES
        self.__trajectory = []
        self.__trajectoryCounter=0
        self.__trajectoryDrawn = False

        # ODOMETRY ATTRIBUTES
        self.__odometryEnabled=False
        self.__odometryDrawn = False

        self._pathFollowing=None
        self._isSpeedLocked=False

    # SETTERS
    def setPose(self,pose:Pose):
        # Sets the current position of the robot
        super().setPose(pose)
        self.setOdometryPose(pose.copy())
        self._frame.setCoordinates(self._pose)
        self.computeRotationCenter()

    def setOdometryPose(self, pose:Pose):
        # Sets the current position of the robot for odometry calculations.
        self.__odometryPose = pose


    def setPathFollowing(self, pathFollowing):
        # Sets the path following controller for the robot.
        self._pathFollowing = pathFollowing

    def setSpeedLock(self, state: bool):
        # Sets the wheels speed lock state (allows or not the change of the speed of the wheels).
        self._isSpeedLocked = state

    # GETTERS
    def getComponents(self) -> List[Component]:
        """ Returns all the components mounted on the robot."""
        return self._components

    @abstractmethod
    def getLeftLinearSpeed(self) -> float:
        """ Returns the left wheel linear speed [px/min]."""
        pass

    @abstractmethod
    def getRightLinearSpeed(self) -> float:
        """ Returns the right wheel linear speed [px/min]."""
        pass

    @abstractmethod
    def getDistanceBetweenWheels(self) -> float:
        """ Returns the distance between the wheels of the robot [px]."""
        pass

    def getTrajectoryDrawn(self) -> bool:
        return self.__trajectoryDrawn

    def getOdometryDrawn(self) -> bool:
        return self.__odometryDrawn

    def getOdometryPose(self) -> Pose:
        """ Returns the odometry estimated position of the robot."""
        return self.__odometryPose

    def getWheels(self) -> List[Wheel]:
        """ Returns all the wheels of a robot."""
        return self._wheels

    def getBoundingWidth(self) -> float:
        """ Returns the bounding width of the robot."""
        return self.getRepresentation().getShape().getBoundingBox().getWidth()

    def getBoundingHeight(self) -> float:
        """ Returns the bounding height of the robot."""
        return self.getRepresentation().getShape().getBoundingBox().getHeigt()

    def getPathFollowing(self):
        return self._pathFollowing

    def addComponent(self, component:Component, x:float=0, y:float=0, orientation:float=0):
        """ Adds a component to a robot.
        @param component  Component to add to the robot
        @param x  x coordinate of the component on the robot [px]
        @param y  y coordinate of the component on the robot [px]
        @param orientation  Orientation of the component on the robot [degrees]"""
        if isinstance(component, Component) and not self.hasComponent(component):
            pose=Pose(-x,y,orientation)
            component.setPose(pose)
            component.setParent(self)
            component.getFrame().setBaseFrame(self._frame)
            component.getFrame().setCoordinates(pose)
            if self._environment is not None:
                component.setEnvironment(self._environment)
                if isinstance(component,Sensor):
                    component.refresh()
                    self._environment.addSensor(component)
            self._components.append(component)
            if isinstance(component,Wheel):
                self._wheels.append(component)
            self._representation.addSubRepresentation(component.getRepresentation())

    def hasComponent(self,component:Component):
        """ Returns True if the component is mounted on the robot; otherwise returns False."""
        return component in self._components

    def move(self):
        # Calculates the displacement of the robot according to the parameters of its wheels. Updates trajectory and odometry
        self.__updateTrajectory()
        self.__updateOdometry()
        self.notifyObservers("stateChanged")

        if self._pathFollowing is not None:
            self._pathFollowing.followPath()

    def visibilityChanged(self):
        for comp in self._components:
            comp.setVisibilityLocked(not self.isVisible())
        if not self.isVisible():
            if self.__odometryDrawn:
                self.__odometryDrawn=False
                self.__hideOdometry()
            if self.__trajectoryDrawn:
                self.__trajectoryDrawn=False
                self.__hideTrajectory()
        super().visibilityChanged()

    def stop(self):
        for wheel in self._wheels:
            wheel.setSpeed(0)

    # TRAJECTORY METHODS
    def __updateTrajectory(self):
        if self.__trajectoryCounter==0:
            point = Object(Representation(Point(self._representation.getShape().getColor())))
            self.__trajectory.append(point)
            if len(self.__trajectory)>=Robot.__MAX_POINTS_NUMBER_IN_ARRAY:
                elt = self.__trajectory.pop(0)
                self._environment.removeVirtualObject(elt)
            if self.__trajectoryDrawn:
                self._environment.addVirtualObject(self.__trajectory[-1], self._pose.getX(), self._pose.getY())
            else:
                self.__trajectory[-1].setPose(Pose(self._pose.getX(), self._pose.getY()))
        self.__trajectoryCounter= (self.__trajectoryCounter + 1) % self.__NUMBER_CALLS_BEFORE_REFRESH

    def __showTrajectory(self):
        # Shows the trajectory of a robot.
        for point in self.__trajectory:
            point_pose=point.getPose()
            self._environment.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def __hideTrajectory(self):
        # Hides the trajectory of a robot.
        for point in self.__trajectory:
            self._environment.removeVirtualObject(point)
        self._drawTrajectory=False

    def deleteTrajectory(self):
        self.__hideTrajectory()
        self.__trajectory.clear()
        self.__trajectoryCounter=0

    def toggleTrajectoryDrawn(self):
        self.__trajectoryDrawn = not self.__trajectoryDrawn
        if self.__trajectoryDrawn:
            self.__showTrajectory()
            return
        self.__hideTrajectory()

    # ODOMETRY METHODS
    def isOdometryEnabled(self):
        """ Returns True if the odometry position estimate is enabled; otherwise returns False.."""
        return self.__odometryEnabled

    def enableOdometry(self,accuracy=1):
        """ Enables the odometry position estimate."""
        if not self.__odometryEnabled:
            self.__odometryEnabled=True
            self.__odometry = []
            self.__odometryCounter = 0
            self.__odometryPose=None
            self.__odometryNoise=1-(accuracy if 0<=accuracy<=1 else 1)
            if self._pose is not None:
                self.__odometryPose=self._pose.copy()

    def disableOdometry(self):
        """ Disables the odometry position estimate."""
        if self.__odometryEnabled:
            self.__odometryEnabled=False
            self.__odometryDrawn = False
            self.__odometryPose=None
            self.deleteOdometry()

    def __updateOdometry(self):
        # Calculates the estimated displacement of the robot according to the parameters of its wheels.
        if self.__odometryEnabled:
            vd = self.getRightLinearSpeed()
            vg = self.getLeftLinearSpeed()

            if self._environment.isReal(): # Adding noise when the environment is real
                vd+=random.uniform(-self.__odometryNoise*vd,self.__odometryNoise*vd)
                vg+=random.uniform(-self.__odometryNoise*vg,self.__odometryNoise*vg)

            v = (vd + vg) / 2
            e = self.getDistanceBetweenWheels()
            d = v * config["real_update_time_step"]/60

            x=self.__odometryPose.getX()
            y=self.__odometryPose.getY()

            if vd != vg and vd!=-vg: # The robot does not go straight ahead and does not turn on the spot
                R = e * (vd + vg) / (vd - vg)
                # Calculation of the coordinates of the center of the trajectory circle
                x0 = x + R * cos(radians(self.__odometryPose.getOrientation()))
                y0 = y + R * sin(radians(self.__odometryPose.getOrientation()))

                # Calculation of the robot position
                dTheta =-d/R
                self.__odometryPose.rotate(degrees(dTheta))
                self.__odometryPose.move(x0 - R * cos(radians(self.__odometryPose.getOrientation())),
                                         y0 - R * sin(radians(self.__odometryPose.getOrientation())))
            elif vd==-vg: # Robot that turns on the spot
                dd=vd * config["real_update_time_step"]/60
                dTheta=-atan(dd/e)
                self.__odometryPose.rotate(degrees(dTheta))
            else: # Robot that moves in a straight line
                nx=x-d * sin(radians(self.__odometryPose.getOrientation()))
                ny=y+d * cos(radians(self.__odometryPose.getOrientation()))
                self.__odometryPose.move(nx, ny)

            if self.__odometryCounter == 0:
                point = Object(Representation(Point(colors["silver"])))
                self.__odometry.append(point)
                if len(self.__odometry) >= Robot.__MAX_POINTS_NUMBER_IN_ARRAY:
                    elt = self.__odometry.pop(0)
                    self._environment.removeVirtualObject(elt)
                if self.__odometryDrawn:
                    self._environment.addVirtualObject(self.__odometry[-1], self.__odometryPose.getX(), self.__odometryPose.getY())
                else:
                    self.__odometry[-1].setPose(Pose(self.__odometryPose.getX(), self.__odometryPose.getY()))
            self.__odometryCounter = (self.__odometryCounter + 1) % self.__NUMBER_CALLS_BEFORE_REFRESH

    def __showOdometry(self):
        if self.__odometryEnabled:
            for point in self.__odometry:
                point_pose = point.getPose()
                self._environment.addVirtualObject(point, point_pose.getX(), point_pose.getY())

    def __hideOdometry(self):
        if self.__odometryEnabled:
            for point in self.__odometry:
                self._environment.removeVirtualObject(point)

    def deleteOdometry(self):
        if self.__odometryEnabled:
            self.__hideOdometry()
            self.__odometry.clear()
            self.__odometryCounter=0

    def toggleOdometryDrawn(self):
        self.__odometryDrawn=not self.__odometryDrawn
        if self.__odometryDrawn:
            self.__showOdometry()
            return
        self.__hideOdometry()

    @abstractmethod
    def computeRotationCenter(self):
        # Computes the rotation center of the robot according to the position of its wheels.
        pass
