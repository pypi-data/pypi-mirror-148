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
from discoverySimulator.representation.shapes.Rectangle import Rectangle


class RectangularObstacle(Obstacle):

    """ The RectangularObstacle class provides a rectangular obstacle.
    It is a comfort class avoiding the manipulation of Shape and Representation classes."""

    def __init__(self,width:float,height:float,color:str=None,borderRadius:float=0,opacity:int=255):
        """ Constructs a rectangular obstacle.
        @param width  Width of the obstacle
        @param height  Height of the obstacle
        @param color  Color of the shape
        @param borderRadius  Border radius of the shape
        @param opacity  Opacity of the shape"""
        rep=Representation(Rectangle(width,height,color,borderRadius,opacity))
        super().__init__(rep)