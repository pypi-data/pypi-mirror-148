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


from discoverySimulator.obstacles import Obstacle
from discoverySimulator.representation.Representation import Representation
from discoverySimulator.representation.shapes.Circle import Circle


class CircularObstacle(Obstacle):

    """ The CircularObstacle class provides a circular obstacle object.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    def __init__(self,radius:float,color:str=None,opacity:int=255):
        """ Constructs a circular obstacle.
        @param radius  Radius of the obstacle
        @param color  Color of the obstacle
        @param opacity  Opacity of the obstacle"""
        rep=Representation(Circle(radius,color,opacity))
        super().__init__(rep)