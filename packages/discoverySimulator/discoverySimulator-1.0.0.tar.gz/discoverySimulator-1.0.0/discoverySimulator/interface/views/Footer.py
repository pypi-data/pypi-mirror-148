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
from PyQt5.QtGui import QIcon, QFont, QPixmap
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QMenuBar, QAction, QLabel, \
    QWidgetAction, QLineEdit, QVBoxLayout, QToolBar

from discoverySimulator.config import *


class Footer(QToolBar):

    __FOOTER_FIXED_HEIGHT = 48

    def __init__(self,zoomController):
        super().__init__()
        self.__zoomController=zoomController
        self.setContentsMargins(0,0,0,0)
        self.setFixedHeight(self.__FOOTER_FIXED_HEIGHT)
        self.setStyleSheet("*{background-color:"+colors['alabaster']+";color:"+colors['tundora']+";border:none;}"
                           "#widget{border-right:1px solid "+colors['silver']+"; margin-top:8px; margin-bottom:8px;}")
        self.addWidget(self.__createZoomMenuWidget())
        self.addWidget(self.__createScaleWidget())
        self.addWidget(self.__createMousePoseWidget())

    def updateZoom(self,sender):
        zoom=round(sender.getZoom()*100)
        self._zoom_edit.setText(f"{zoom}%")
        self._zoom_text.setText(f"{zoom}%")
        self._scale_text.setText(str(round(100/sender.getZoom())))

    def updateMousePoseFromScene(self,scene):
        mouse=scene.mousePose()
        self._pose_text.setText(f"({mouse.x()}, {mouse.y()})")

    def menuOpened(self):
        self._zoom_edit.selectAll()
        self._zoom_edit.setFocus()

    def __createZoomMenuWidget(self) -> QWidget:
        zoomWidget=QWidget()
        zoomWidget.setContentsMargins(12,0,12,0)
        zoomWidget.setFixedWidth(138)
        zoomWidget.setObjectName("widget")

        zoomLayout=QHBoxLayout(zoomWidget)
        zoomLayout.setAlignment(Qt.AlignCenter)

        self._zoom_text = QLabel("100%")
        self._zoom_text.setAlignment(Qt.AlignRight)
        self._zoom_text.setFont(fonts["normal_bold"])
        self._zoom_text.setFixedWidth(56)

        zoomMenuBar=QMenuBar()
        zoomMenuBar.setContentsMargins(0,0,0,0)
        zoomMenuBar.setStyleSheet("QMenu::item:selected{background-color:"+colors["picton-blue"]+"; color:"+colors["white"]+";}")

        self._zoomMenu=zoomMenuBar.addMenu("")
        self._zoomMenu.aboutToShow.connect(self.menuOpened)

        self._zoomMenu.setIcon(QIcon(os.path.join(config["ressourcesPath"],'footer','arrowUp.svg')))

        # ACTIONS
        zoom_in = QAction("Zoom in", self)
        zoom_in.setShortcut("ctrl++")
        zoom_in.triggered.connect(self.__zoomController.zoomIn)

        zoom_out = QAction("Zoom out", self)
        zoom_out.setShortcut("ctrl+-")
        zoom_out.triggered.connect(self.__zoomController.zoomOut)

        zoom_to_fit = QAction("Zoom to fit", self)
        zoom_to_fit.triggered.connect(self.__zoomController.zoomToFit)

        zoom_input = QWidgetAction(self)
        self._zoom_edit = QLineEdit()
        self._zoom_edit.setText("100%")
        self._zoom_edit.setStyleSheet("border: none")
        self._zoom_edit.editingFinished.connect(self.__zoomInputChanged)

        zoom_input.setDefaultWidget(self._zoom_edit)

        self._zoomMenu.addAction(zoom_input)
        self._zoomMenu.addSeparator()
        self._zoomMenu.addAction(zoom_in)
        self._zoomMenu.addAction(zoom_out)
        self._zoomMenu.addAction(zoom_to_fit)

        zoomLayout.addWidget(self._zoom_text)
        zoomLayout.addWidget(zoomMenuBar)

        return zoomWidget

    def __createScaleWidget(self) -> QWidget:
        scaleWidget = QWidget()
        scaleWidget.setObjectName("widget")
        scaleLayout = QVBoxLayout(scaleWidget)
        scaleLayout.setSpacing(0)
        self._scale_text = QLabel("100")

        self._scale_text.setFont(fonts["small_bold"])
        self._scale_text.setAlignment(Qt.AlignCenter)
        scaleIcon = QLabel()
        scaleIcon.setPixmap(QPixmap(os.path.join(config["ressourcesPath"],'footer','scale.svg')))
        scaleIcon.setFixedSize(100, 12)

        scaleLayout.addWidget(self._scale_text)
        scaleLayout.addWidget(scaleIcon)

        scaleLayout.setSpacing(0)
        scaleWidget.setContentsMargins(12, 0, 12, 0)

        return scaleWidget

    def __createMousePoseWidget(self) -> QWidget:
        poseWidget = QWidget()
        poseLayout = QHBoxLayout()
        poseWidget.setLayout(poseLayout)
        poseWidget.setLayoutDirection(Qt.LayoutDirection(0))

        self._pose_text = QLabel("(0, 0)")
        self._pose_text.setStyleSheet("margin-left:8px;")
        self._pose_text.setFont(fonts["normal_bold"])

        poseIcon = QLabel()
        poseIcon.setPixmap(QPixmap(os.path.join(config["ressourcesPath"],'footer','mousePose.svg')))

        poseLayout.addWidget(poseIcon)
        poseLayout.addWidget(self._pose_text)

        poseLayout.setSpacing(0)
        poseWidget.setContentsMargins(12,0,12,0)

        return poseWidget

    def __zoomInputChanged(self):
        text=self._zoom_edit.text()
        if text[-1]=='%':
            text=text.rstrip('%')
        if text.isnumeric():
            zoom=int(text)/100
            if self.__zoomController.setZoom(zoom):
                self._zoomMenu.close()
        else:
            self._zoom_edit.setText(f"{int(self.__zoomController.getZoom() * 100)}%")

