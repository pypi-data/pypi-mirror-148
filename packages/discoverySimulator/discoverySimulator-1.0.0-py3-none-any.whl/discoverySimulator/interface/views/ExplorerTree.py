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
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem

from discoverySimulator.config import *
from discoverySimulator.interface.components.Button import VisibilityButton
from discoverySimulator.Object import Object
from discoverySimulator.robots.Robot import Robot
from discoverySimulator.obstacles.Obstacle import Obstacle
from discoverySimulator.sensors.Sensor import Sensor
from discoverySimulator.actuators.Actuator import Actuator


class ExplorerTree(QTreeWidget):

    __ALL_ITEMS = [Robot, Actuator, Sensor, Obstacle]

    def __init__(self,environment,parent):
        super().__init__()
        self.setStyleSheet("QTreeView::item:hover,QTreeView::item:selected{color:"+colors["mischka"]+"; background-color:#"+colors["picton-blue"]+";}")

        self.__environment = environment
        self.__mainItems=[]
        self.__subItems=[]
        self.__allObjects = []
        self.__mainObjects=[]
        self.__childrenButtons=[]
        self.__mainItemsAssociatedChildren=[]
        self.__visibilityButtons=[]
        self.__parent=parent
        self.__selectedItem=None
        self.__selectedSubItem=None
        self.__itemsShown=ExplorerTree.__ALL_ITEMS

        self.__setTreeWidgetConfiguration()
        self.__buildTree()

    def __setTreeWidgetConfiguration(self):
        self.setHeaderHidden(True)
        self.setColumnCount(2)
        self.setColumnWidth(0, 300)
        self.setAutoScroll(True)
        self.resizeColumnToContents(1)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def rebuildTree(self,sender):
        if hasattr(sender,"getShownObjectClasses"):
            self.__itemsShown=sender.getShownObjectClasses()
        self.__clearTree()
        self.__buildTree()
        self.expandAll()

    def __clearTree(self):
        if self.__selectedItem is not None:
            self.__mainObjects[self.__mainItems.index(self.__selectedItem)].setSelected(False)
        self.__removeSelectedItem()
        self.itemClicked.disconnect(self.__clickedItem)

        root = self.invisibleRootItem()
        parents = []
        for i in range(root.childCount()):
            parents.append(root.child(i))
            childs = []
            for j in range(parents[-1].childCount()):
                childs.append(parents[-1].child(j))
            for child in childs:
                parents[-1].removeChild(child)
        for parent in parents:
            root.removeChild(parent)

        self.__mainItems.clear()
        self.__subItems.clear()
        self.__allObjects.clear()
        self.__mainObjects.clear()
        self.__childrenButtons.clear()
        self.__mainItemsAssociatedChildren.clear()
        self.__visibilityButtons.clear()

    def __buildTree(self):
        for obj in self.__environment.getObjects():
             if type(obj) != Object:
                if issubclass(type(obj), tuple(self.__itemsShown)) or (isinstance(obj, Robot) and (Actuator in self.__itemsShown or Sensor in self.__itemsShown)):
                    parent=None
                    if not issubclass(type(obj), tuple(self.__itemsShown)) and isinstance(obj, Robot) and (Actuator in self.__itemsShown or Sensor in self.__itemsShown):
                        sensors = [comp for comp in obj.getComponents() if isinstance(comp,Sensor)]
                        if (Sensor in self.__itemsShown and sensors) or (Actuator in self.__itemsShown and len(obj.getComponents()) - len(sensors) != 0):
                            parent = Item(self, obj.getID())
                            parent.setIcon(0,QIcon(os.path.join(config["ressourcesPath"],'objects','robotDisabled.svg')))
                            self.__visibilityButtons.append(None)
                    else:
                        parent = Item(self, obj.getID())
                        classname = [item for item in self.__itemsShown if isinstance(obj, item)][0].__name__
                        parent.setIcon(0,QIcon(os.path.join(config["ressourcesPath"],'objects',f'{classname.lower()}.svg')))
                        self.__visibilityButtons.append(VisibilityButton(obj.isVisible()))
                        self.setItemWidget(parent, 1, self.__visibilityButtons[-1])

                    if parent is not None:
                        parent.setFont(fonts["normal_bold"])

                        self.__mainItems.append(parent)
                        self.__mainObjects.append(obj)
                        self.__allObjects.append(obj)
                        self.__mainItemsAssociatedChildren.append([])
                        self.__childrenButtons.append([])

                        if hasattr(obj,"getComponents"):
                            for comp in obj.getComponents():
                                if issubclass(type(comp), tuple(self.__itemsShown)):
                                    child = Item(parent,comp.getID())
                                    self.__visibilityButtons.append(VisibilityButton(comp.isVisible()))
                                    if comp.getVisibilityLocked():
                                        self.__visibilityButtons[-1].lock()
                                    self.setItemWidget(child, 1, self.__visibilityButtons[-1])
                                    self.__subItems.append(child)
                                    self.__mainItemsAssociatedChildren[-1].append(child)
                                    self.__childrenButtons[-1].append(self.__visibilityButtons[-1])
                                    self.__allObjects.append(comp)
                                    parent.addChild(child)
                                    classname = [item for item in self.__itemsShown if isinstance(comp, item)][0].__name__
                                    child.setIcon(0,QIcon(os.path.join(config["ressourcesPath"],'objects',f'{classname.lower()}.svg')))

        for button in self.__visibilityButtons:
            if button is not None:
                button.clicked.connect(self.__toggleObjectVisibily)
        self.itemClicked.connect(self.__clickedItem)

    def __clickedItem(self):
        crawler = self.currentItem()
        if self.__selectedItem is not None:
            self.__mainObjects[self.__mainItems.index(self.__selectedItem)].setSelected(False)
        if crawler in self.__mainItems:
            selectedObject = self.__mainObjects[self.__mainItems.index(crawler)]
        else:
            selectedObject = self.__mainObjects[[i for i in range(len(self.__mainItems)) if crawler in self.__mainItemsAssociatedChildren[i]][0]]
            crawler.setColor(colors['mischka'])
            self.__selectedSubItem=crawler
        selectedObject.setSelected(True)

    def __setSelectedItem(self, item):
        item.setColor(colors['mischka'])
        item.setExpanded(True)
        self.setCurrentItem(item)
        self.__selectedItem=item
        if self.__selectedSubItem is not None:
            self.__parent.showExplorerInfo(self.__allObjects[1 + self.__mainItems.index(self.__selectedItem) + self.__subItems.index(self.__selectedSubItem)])
        else:
            self.__parent.showExplorerInfo(self.__mainObjects[self.__mainItems.index(self.__selectedItem)])

    def __removeSelectedItem(self):
        if self.__selectedItem is not None:
            self.clearSelection()
            self.__selectedItem.setColor(colors['mid-gray'])

            for subItem in self.__subItems:
                subItem.setColor(colors['mid-gray'])

            if self.__selectedSubItem is not None:
                self.__parent.hideExplorerInfo(self.__allObjects[1 + self.__mainItems.index(self.__selectedItem) + self.__subItems.index(self.__selectedSubItem)])
            else:
                self.__parent.hideExplorerInfo(self.__mainObjects[self.__mainItems.index(self.__selectedItem)])
            self.__selectedItem=None
            self.__selectedSubItem=None

    def changeTreeSelection(self,sender):
        if sender in self.__mainObjects:
            crawler = self.__mainItems[self.__mainObjects.index(sender)]
            if sender.isSelected():
                self.__setSelectedItem(crawler)
            else:
                self.__removeSelectedItem()

    def changeTreeVisibility(self,sender):
        if sender in self.__allObjects:
            button=self.__visibilityButtons[self.__allObjects.index(sender)]
            button.setState(sender.isVisible())

            if sender in self.__mainObjects:
                children_buttons = self.__childrenButtons[self.__mainObjects.index(sender)]
                if sender.isVisible():
                    for children_button in children_buttons:
                        children_button.unlock()
                else:
                    for children_button in children_buttons:
                        children_button.lock()

    def __toggleObjectVisibily(self):
        button = self.sender()
        obj = self.__allObjects[self.__visibilityButtons.index(button)]
        obj.toggleVisible()


class Item(QTreeWidgetItem):

    def __init__(self,parent, txt='', color=colors['mid-gray']):
        super().__init__(parent)
        self.setColor(color)
        self.setText(0,txt)
        self.setFont(fonts["normal"])

    def setFont(self,fnt,col=0):
        super().setFont(col,fnt)

    def setColor(self,color):
        self.setForeground(0,QColor(color))


