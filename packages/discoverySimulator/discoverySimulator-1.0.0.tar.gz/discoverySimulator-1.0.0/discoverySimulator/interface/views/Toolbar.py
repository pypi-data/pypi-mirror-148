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


from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QToolBar, QLabel, QHBoxLayout, QWidget, QLineEdit, QWidgetAction
from discoverySimulator.Observable import Observable
from discoverySimulator.config import *
from discoverySimulator.interface.components.Button import Button, PlayButton
from discoverySimulator.interface.views.About import About
from discoverySimulator.robots import Robot


class Toolbar(QToolBar,Observable):

    __TOOLSBAR_FIXED_HEIGHT = 48

    def __init__(self,simulation):
        super().__init__()
        self.setFixedHeight(self.__TOOLSBAR_FIXED_HEIGHT)
        self.setStyleSheet("*{background-color: "+colors["steel-gray"]+";color:"+colors["gallery"]+";border:none;}"
                           "#widget{border-right:1px solid #4D4D6D; margin-top:8px; margin-bottom:8px;}")

        self.__simulation=simulation

        self.__robotTitleWidget=None
        self.__pathFollowingWidget=None

        self.setContentsMargins(0,0,0,0)
        self.addWidget(self.__createAboutWidget())

        self.addAction(self.__createSectionTitleWidget("Simulation"))
        self.addWidget(self.__createTimerWidget())
        self.addWidget(self.__createAccelerationWidget())
        self.addWidget(self.__createPlayPauseWidget())

        self.__robotTitleWidget = self.__createSectionTitleWidget("Robot")
        self.__pathFollowingWidget=self.pathFollowingWidget()
        self.__robotSelected=None

    # GETTERS

    def getRobotSelected(self) -> Robot:
        return self.__robotSelected


    def updateTimeElapsed(self,sender):
        time=sender.time()
        hours=int(time//3600)
        time-=hours*3600
        minutes=int(time//60)
        time-=minutes*60
        seconds=time

        str=""
        if hours>0:
            str+=f"{hours}h"
        if minutes>0 or hours>0:
            str+=f"{'0' if minutes<10 and hours>0 else ''}{minutes}min"
        str+=f"{'0' if seconds<10 and  (minutes>0 or hours>0) else ''}{round(seconds,1) if minutes==0 else int(seconds)}s"
        self._timeElapsed.setText(str)

    def __createSectionTitleWidget(self, name="") -> QWidgetAction:
        labelWidget = QWidgetAction(self)
        label=QLabel(name+":")
        label.setFont(fonts["normal"])
        label.setStyleSheet("color:"+colors['white']+"; border-left:1px solid"+colors['mulled-wine']+";")
        label.setContentsMargins(8,0,0,0)
        labelWidget.setDefaultWidget(label)
        return labelWidget

    def __createAboutWidget(self) -> QWidget:
        about=QWidget()
        about_layout=QHBoxLayout(about)

        about_layout.setSpacing(0)
        about.setContentsMargins(4, 0, 4, 0)
        about_button = Button()
        about_button.setIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','about.svg')))
        about_button.setIconSize(QSize(22, 22))
        about_button.clicked.connect(self.__openPopUp)
        about_button.setToolTip("About")
        about_layout.addWidget(about_button)
        about.setFixedHeight(self.__TOOLSBAR_FIXED_HEIGHT)

        return about

    def __openPopUp(self):
        About()

    def __createTimerWidget(self) -> QWidget:
        timer_icon=QLabel()
        timer_icon.setStyleSheet("image: url("+os.path.join(config['ressourcesPath'],'toolbar','timer.svg').replace('\\','/')+");"
                                 "image-repeat:no-repeat; image-position:center; image-size:contain;")
        timer_icon.setFixedWidth(16)

        timer = QWidget()
        timer.setObjectName("widget")
        timer_layout=QHBoxLayout(timer)

        timer_layout.setSpacing(0)
        timer.setContentsMargins(4,0,4,0)

        self._timeElapsed=QLabel()
        self._timeElapsed.setStyleSheet("margin-left:8px;")

        timer_layout.addWidget(timer_icon)
        timer_layout.addWidget(self._timeElapsed)

        timer_layout.setAlignment(Qt.AlignLeft)

        self._timeElapsed.setFont(fonts["normal"])

        self.updateTimeElapsed(self.__simulation)

        return timer

    def __createAccelerationWidget(self) -> QWidget:
        accelerationWidget=QWidget()
        accelerationWidget.setObjectName("widget")

        layout=QHBoxLayout(accelerationWidget)
        layout.setSpacing(0)
        accelerationWidget.setContentsMargins(4,0,4,0)

        decreaseButton = Button()
        decreaseButton.setIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','decreaseAcceleration.svg')))
        decreaseButton.setToolTip("Decrease Acceleration")
        decreaseButton.clicked.connect(self.__simulation.decreaseAcceleration)

        self.__accelerationTextInput = QLineEdit(f"x{self.__simulation.getAcceleration()}")
        self.__accelerationTextInput.setMaxLength(5)
        self.__accelerationTextInput.setFont(fonts["normal"])
        self.__accelerationTextInput.setAlignment(Qt.AlignCenter)
        self.__accelerationTextInput.editingFinished.connect(self.__inputValueAcceleration)

        increaseButton=Button()
        increaseButton.setIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','increaseAcceleration.svg')))
        increaseButton.setToolTip("Increase Acceleration")
        increaseButton.clicked.connect(self.__simulation.increaseAcceleration)

        layout.addWidget(decreaseButton)
        layout.addWidget(self.__accelerationTextInput)
        layout.addWidget(increaseButton)

        accelerationWidget.setFixedWidth(132)

        return accelerationWidget

    def __inputValueAcceleration(self):
        self.__simulation.setAccelerationFromString(self.__accelerationTextInput.text())

    def updateAcceleration(self,sender):
        self.__accelerationTextInput.setText(f'x{sender.getAcceleration()}')
        self.__accelerationTextInput.clearFocus()

    def __createPlayPauseWidget(self) -> QWidget:
        playWidget = QWidget()
        play_layout=QHBoxLayout(playWidget)
        play_layout.setSpacing(0)
        playWidget.setContentsMargins(4, 0, 4, 0)

        playState=self.__simulation.getPlayState()
        self._playPauseButton = PlayButton(playState)
        self._playPauseButton.setToolTip("Pause" if playState else "Play")
        self._playPauseButton.clicked.connect(self.__simulation.togglePlayState)

        play_layout.addWidget(self._playPauseButton)
        return playWidget

    def updatePlayState(self,sender):
        playState=sender.getPlayState()
        self._playPauseButton.setToolTip("Pause" if playState else "Play")
        self._playPauseButton.setState(playState)

    def robotSelected(self,sender):
        if sender.isSelected():
            self.__robotSelected=sender
            self.__pathFollowingButtonState = False
            self.addAction(self.__robotTitleWidget)
            self.addAction(self.__pathFollowingWidget)
        else:
            self.removeAction(self.__robotTitleWidget)
            self.removeAction(self.__pathFollowingWidget)

    def pathFollowingWidget(self) -> QWidgetAction:
        widget=QWidgetAction(self)
        self.__pathFollowingButton = Button()
        widget.setDefaultWidget(self.__pathFollowingButton)
        self.__pathFollowingButton.setIcon(QIcon(os.path.join(config['ressourcesPath'],'toolbar','goTo.svg')))
        self.__pathFollowingButton.setToolTip("Go To")
        self.__pathFollowingButton.clicked.connect(self.__clickedFollowPath)
        return widget

    def __clickedFollowPath(self):
        self.__pathFollowingButtonState = not self.__pathFollowingButtonState
        self.__pathFollowingButton.setDown(self.__pathFollowingButtonState)
        self.notifyObservers('followPathSelected')



