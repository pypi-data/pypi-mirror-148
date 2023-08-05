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
from discoverySimulator.Object import Object

class Component(ABC,Object):

    """ The Component class provides a mold to implement components."""

    def __init__(self,representation):
        """ Constructs a component.
        @param representation  Representation of the component."""
        super().__init__(representation)
        self._parent = None

    # SETTERS
    def setParent(self,parent):
        self._parent = parent

    # GETTERS
    @abstractmethod
    def getSpecifications(self):
        pass


