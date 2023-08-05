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


from discoverySimulator.Observable import Observable
from PyQt5.QtCore import QPoint, QSize


class ZoomController(Observable):

    __ZOOM_STEP = 0.1
    __ZOOM_MIN = 0.1
    __ZOOM_MAX  = 3.0

    def __init__(self,environnement):
        super().__init__()
        self.__environnementSize = environnement.getSize()
        self.__sceneSize = None
        self.__sceneOverviewSize = None

        self.__sceneOverviewFitted=False

        self.__zoom=1.0
        self.__zoomToFit = 1.0
        self.__overviewZoom=1.0

        self.__offset=QPoint(0, 0)
        self.__overviewOffset=QPoint(0, 0)

    def setZoom(self, zoom:float):
        if zoom >= ZoomController.__ZOOM_MIN and zoom <= ZoomController.__ZOOM_MAX:
            self.__zoom = zoom
            self.zoomChanged()
            return True
        if zoom > self.__ZOOM_MAX:
            self.__zoom = ZoomController.__ZOOM_MAX
            self.zoomChanged()
            return True
        return False

    def setSceneSize(self, size:QSize):
        self.__sceneSize = size
        self.__zoomToFit = min(self.__sceneSize.width() / self.__environnementSize.width(), self.__sceneSize.height() / self.__environnementSize.height())
        ZoomController.__ZOOM_MAX=max(self.__zoomToFit,ZoomController.__ZOOM_MAX)
        if self.__offset.isNull():
            off = (self.__sceneSize-self.__environnementSize)/2
            if off.width()>0 and off.height()>0:
                self.__offset=QPoint(off.width(),off.height())

    def setSceneOverviewSize(self, size:QSize):
        self.__sceneOverviewSize = size

    def setOffset(self, offset:QPoint):
        self.__offset = offset

    def getZoom(self):
        return self.__zoom

    def getZoomOverview(self):
        return self.__overviewZoom

    def getOffset(self) -> QPoint:
        return self.__offset

    def getOverviewOffset(self) -> QPoint:
        return self.__overviewOffset

    def getSceneSize(self):
        return self.__sceneSize

    def zoomIn(self):
        self.__zoom+=ZoomController.__ZOOM_STEP
        self.__zoom = min(self.__zoom, ZoomController.__ZOOM_MAX)
        self.zoomChanged()

    def zoomOut(self):
        self.__zoom-=ZoomController.__ZOOM_STEP
        self.__zoom = max(self.__zoom, ZoomController.__ZOOM_MIN)
        self.zoomChanged()

    def zoomToFit(self):
        self.__zoom=self.__zoomToFit
        off = (self.__sceneSize - self.__environnementSize*self.__zoom) / 2
        self.__offset = QPoint(off.width(), off.height())
        self.zoomChanged()

    def zoomOverviewToFit(self):
        if not self.__sceneOverviewFitted:
            self.__sceneOverviewFitted=True

            delta = self.__sceneSize - self.__environnementSize
            if delta.width()<0 or delta.height()<0:
                self.__overviewZoom=min(self.__sceneOverviewSize.width() / self.__environnementSize.width(), self.__sceneOverviewSize.height() / self.__environnementSize.height())
            else:
                self.__overviewZoom=min(self.__sceneOverviewSize.width() / self.__sceneSize.width(), self.__sceneOverviewSize.height() / self.__sceneSize.height())
            off = (self.__sceneOverviewSize - self.__environnementSize * self.__overviewZoom) / 2
            self.__overviewOffset = QPoint(off.width(), off.height())

    def zoomChanged(self):
        self.notifyObservers("zoomChanged")