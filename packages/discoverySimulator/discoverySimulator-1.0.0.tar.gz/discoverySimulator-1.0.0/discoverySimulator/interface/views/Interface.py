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


from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout
from discoverySimulator.ZoomController import ZoomController
from discoverySimulator.config import *
from discoverySimulator.interface.views.Footer import Footer
from discoverySimulator.interface.views.Scene import Scene
from discoverySimulator.interface.views.Explorer import Explorer
from discoverySimulator.interface.views.SceneOverview import SceneOverview
from discoverySimulator.interface.views.Toolbar import Toolbar

class Interface(QMainWindow):
    def __init__(self,simulation,environment):
        super().__init__()
        self.setWindowTitle(config["appname"])
        self.setWindowIcon(QIcon(os.path.join(config["ressourcesPath"],'window.svg')))

        self.__simulation = simulation
        self.__environment = environment

        general_widget=QWidget()

        self.__general_layout=QGridLayout(general_widget)
        self.__general_layout.setContentsMargins(0, 0, 0, 0)
        self.__general_layout.setSpacing(0)

        zoomController = ZoomController(self.__environment)

        self.__toolbarWidget = Toolbar(self.__simulation)
        self.__sceneWidget=Scene(self.__environment, zoomController)
        sceneOverviewWidget = SceneOverview(self.__environment, zoomController)
        self.__explorerWidget = Explorer(self.__environment)
        self.__footerWidget = Footer(zoomController)

        zoomController.setSceneOverviewSize(sceneOverviewWidget.size())

        self.__general_layout.addWidget(self.__toolbarWidget, 0, 0, 1, 2)
        self.__general_layout.addWidget(self.__sceneWidget, 1, 0)
        self.__general_layout.addWidget(sceneOverviewWidget, 1, 0, Qt.AlignRight | Qt.AlignBottom)
        self.__general_layout.addWidget(self.__explorerWidget, 1, 1)
        self.__general_layout.addWidget(self.__footerWidget, 2, 0, 1, 2)

        # NOTIFICATION CONNECTIONS
        zoomController.addObserverCallback(self.__footerWidget.updateZoom, "zoomChanged")

        self.__simulation.addObserverCallback(self.__toolbarWidget.updateTimeElapsed, "timeChanged")
        self.__simulation.addObserverCallback(self.__toolbarWidget.updateAcceleration,"accelerationChanged")
        self.__simulation.addObserverCallback(self.__toolbarWidget.updatePlayState, "playStateChanged")

        self.__toolbarWidget.addObserverCallback(self.__sceneWidget.followPathSelected, 'followPathSelected')

        self.__sceneWidget.addObserverCallback(self.__footerWidget.updateMousePoseFromScene, "poseChanged")

        self.__explorerWidget.getExplorerToolsbar().addObserverCallback(self.__sceneWidget.updateLockedScene, "lockChanged")
        self.__explorerWidget.getExplorerToolsbar().addObserverCallback(self.__explorerWidget.getExplorerTree().rebuildTree, 'filterChanged')

        for obj in self.__environment.getObjects():
            obj.addObserverCallback(self.__explorerWidget.getExplorerTree().changeTreeSelection, "selectionChanged")
            obj.addObserverCallback(self.__explorerWidget.getExplorerTree().changeTreeVisibility, "visibilityChanged")
            if hasattr(obj, "getComponents"):
                for comp in obj.getComponents():
                    comp.addObserverCallback(self.__explorerWidget.getExplorerTree().changeTreeVisibility,"visibilityChanged")
                obj.addObserverCallback(self.__toolbarWidget.robotSelected, 'selectionChanged')

        self.setCentralWidget(general_widget)
        self.showMaximized()
        self.__sceneWidget.maximized()

    def closeEvent(self, event):
        self.__simulation.setAppShown(False)
