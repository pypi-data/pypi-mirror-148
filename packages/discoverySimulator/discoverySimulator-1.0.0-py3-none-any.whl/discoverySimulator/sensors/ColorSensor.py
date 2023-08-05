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


from PyQt5.QtCore import QPoint

from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle
from discoverySimulator.sensors import Sensor

class ColorSensor(Sensor):

    """ The ColorSensor class provides the representation and the behavior of a color sensor."""

    def __init__(self,color:str=None):
        """ Constructs a color sensor.
        @param color  Color of the sensor [hex]"""
        self._representation = Representation(Circle(1,color))
        super().__init__(self._representation)
        self._colorDetected = None

    # GETTERS
    def getValue(self) -> str:
        """ Returns the captured color by the sensor."""
        return self._colorDetected

    def getSpecifications(self):
        return "Current detected color : " + self._colorDetected

    def refresh(self):
        previousColor=self._colorDetected
        self._colorDetected=None
        sensorPose = self._frame.getAbsoluteCoordinates()
        colorSensorPoint = QPoint(round(sensorPose.getX()),round(sensorPose.getY()))
        virtualObjects = sorted(self._environment.getVirtualObjects(), key=lambda obj:obj.getZIndex())
        for obj in virtualObjects:
            if obj.getZIndex()<=self._parent.getZIndex():
                if obj.getRepresentation().contains(colorSensorPoint):
                    self._colorDetected = obj.getRepresentation().getShape().getColor()
        if self._colorDetected is None:
            self._colorDetected = colors['gallery']
        if self._colorDetected!=previousColor:
            self.notifyObservers("stateChanged")












