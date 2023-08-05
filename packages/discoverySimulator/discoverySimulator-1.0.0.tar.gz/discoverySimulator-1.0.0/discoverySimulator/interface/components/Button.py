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
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QPushButton

from discoverySimulator.config import *


class Button(QPushButton):

    __BUTTON_SIZE = 24
    __ICON_SIZE = 18

    def __init__(self):
         super().__init__()
         self.setFlat(True)

         self.setFixedSize(QSize(Button.__BUTTON_SIZE,Button.__BUTTON_SIZE))
         self.setIconSize(QSize(Button.__ICON_SIZE,Button.__ICON_SIZE))
         self.setStyleSheet("QPushButton{border-radius:2px;}"
                            "QPushButton:hover{background-color:"+colors["tuna"]+";}"
                            "QPushButton:pressed{background-color:"+colors["mulled-wine"]+";}")

class ToggleButton(Button):
    def __init__(self,state=True):
        super().__init__()
        self._state=state
        self._trueStateIcon=None
        self._falseStateIcon=None

    def setStateIcon(self):
        if self._state:
            if self._trueStateIcon is not None:
                self.setIcon(self._trueStateIcon)
        else:
            if self._falseStateIcon is not None:
                self.setIcon(self._falseStateIcon)

    def setState(self,state):
        self._state=state
        self.setStateIcon()

    def setTrueStateIcon(self,icon):
        self._trueStateIcon=icon
        self.setStateIcon()

    def setFalseStateIcon(self,icon):
        self._falseStateIcon=icon
        self.setStateIcon()


class VisibilityButton(ToggleButton):

    def __init__(self,visibility=True):
        super().__init__(visibility)
        self.setTrueStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','visible.svg')))
        self.setFalseStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','invisible.svg')))

    def lock(self):
        self.setDisabled(True)
        self.setIcon(QIcon(os.path.join(config['ressourcesPath'],'states','point.svg')))

    def unlock(self):
        self.setDisabled(False)
        self.setStateIcon()

class LockButton(ToggleButton):

    def __init__(self,lock=False):
        super().__init__(lock)
        self.setTrueStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','lock.svg')))
        self.setFalseStateIcon(QIcon(os.path.join(config['ressourcesPath'],'states','unlock.svg')))

class PlayButton(ToggleButton):

    def __init__(self,play=False):
        super().__init__(play)
        self.setTrueStateIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','pause.svg')))
        self.setFalseStateIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','play.svg')))