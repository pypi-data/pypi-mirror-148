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


from . import Actuator
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Circle


class LED(Actuator):

    """ The LED class provides the representation and the behavior of an LED.
    The LED can have the desired color and its state can be chosen at will (ON or OFF)."""

    RED = colors["red"]
    GREEN = colors["green"]
    BLUE = colors["blue"]
    YELLOW = colors["yellow"]

    LOW=False
    HIGH=True

    __LOW_OPACITY=56
    __HIGH_OPACITY=255

    def __init__(self,color:str=None):
        """ Constructs a LED.
        @param color  Color of the LED [hex]"""
        self._representation = Representation(Circle(5,LED.RED if color is None else color,20))
        super().__init__(self._representation)
        self.__state=False

    # SETTERS
    def setState(self,state:bool):
        """" Sets the state of the LED with a boolean.
        @param state  State of the LED: True to turn ON the LED, False to turn OFF"""
        if state!=self.__state:
            self.__state=state
            if self.__state==LED.HIGH:
                self._representation.getShape().setOpacity(LED.__HIGH_OPACITY)
            else:
                self._representation.getShape().setOpacity(LED.__LOW_OPACITY)
        self.notifyObservers("stateChanged")

    def toggleState(self):
        """ Toggles the state of the LED."""
        self.setState(not self.__state)

    # GETTERS
    def getState(self) -> bool:
        """ Returns the state of the LED."""
        return self.__state

    def getSpecifications(self) -> str:
        return f"Current state : {'ON' if self.__state else 'OFF'}"



