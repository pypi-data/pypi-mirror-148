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

from discoverySimulator import Object
from discoverySimulator.config import colors
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Line


class Maze:

    """ The Maze class provides a maze."""

    __DEFAULT_BORDER_SCREEN_WIDTH = 2
    __INTERVAL_SIZE = 300

    def __init__(self,environment):
        """ Constructs a maze in the given environment.
        @param environment  Environment where the maze will be added
        """
        self._environment = environment
        self._width = self._environment.getSize().width()
        self._height = self._environment.getSize().height()
        self._nbColumn = self._width//Maze.__INTERVAL_SIZE
        self._nbLine = self._height//Maze.__INTERVAL_SIZE
        self._mazeElements = []

    def draw(self):
        """ Draws the maze."""
        for i in range(self._nbLine+1):
            for j in range(self._nbColumn+1):
                if random.randint(0,1):
                    if j!=0:
                        dh=self._height%Maze.__INTERVAL_SIZE if i == self._nbLine else Maze.__INTERVAL_SIZE
                        self._mazeElements.append(Object(Representation(Line(dh, Maze.__DEFAULT_BORDER_SCREEN_WIDTH,colors['tundora']))))
                        self._environment.addObject(self._mazeElements[-1], j * Maze.__INTERVAL_SIZE, i * Maze.__INTERVAL_SIZE)
                else:
                    if i!=0:
                        dw=self._width%Maze.__INTERVAL_SIZE if j == self._nbColumn else Maze.__INTERVAL_SIZE
                        self._mazeElements.append(Object(Representation(Line(dw, Maze.__DEFAULT_BORDER_SCREEN_WIDTH,colors['tundora']))))
                        self._environment.addObject(self._mazeElements[-1], j * Maze.__INTERVAL_SIZE, i * Maze.__INTERVAL_SIZE, -90)

    def delete(self):
        """ Deletes the maze."""
        for item in self._mazeElements:
            self._environment.removeObject(item)
        self._mazeElements.clear()



