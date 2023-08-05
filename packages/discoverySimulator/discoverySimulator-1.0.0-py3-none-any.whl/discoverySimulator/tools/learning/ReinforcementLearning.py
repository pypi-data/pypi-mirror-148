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
from typing import List
import json


class ReinforcementLearning:

    """ The ReinforcementLearning class provides a reinforcement learning tool. """

    DEFAULT_LEARNING_FACTOR = 0.1
    DEFAULT_DISCOUNT_FACTOR = 0.5
    DEFAULT_EXPLORATION_RATE_DECREASE_FACTOR = 0.995

    __ACTION_BLUIDER_REQUIRED_KEYS = ['intervals', 'max', 'min']

    # Available algorithms : QLearning, ValueIteration
    def __init__(self, state:tuple, actionSpaceBuilders:List[dict]=None, factors:dict=None, algorithm:str= "ValueIteration"):
        """ Constructs a reinforcement learning tool.
        @param state  State of the learning
        """

        self._learn = self.__getattribute__(f"_learn{algorithm}") # Raises an error if not found

        self.__actionSpaceBuilders=actionSpaceBuilders
        self.__actions = None

        self._QTable={}
        self._RTable={}
        self._actionCountTable = {}
        self._explorationRate = 0
        if self.__actionSpaceBuilders is not None and self.__areActionBuildersValid():
            self.__actions=self.getActionsSpace()
            self.fillTable("_QTable")
            self.fillTable("_RTable")
            self.fillTable("_actionCountTable")
            self._explorationRate = 1

        if factors is None:
            factors = {}
        self._factors={
            'learning':ReinforcementLearning.DEFAULT_LEARNING_FACTOR,
            'discount':ReinforcementLearning.DEFAULT_DISCOUNT_FACTOR,
            'explorationRateDecrease':ReinforcementLearning.DEFAULT_EXPLORATION_RATE_DECREASE_FACTOR
        }
        self._factors.update(factors)

        self._state = state
        self._initialState = state


    def __areActionBuildersValid(self):
        if not self.__actionSpaceBuilders:
            raise ValueError(f"Missing key in actionSpaceBuilder item. Required keys are: {', '.join(ReinforcementLearning.__ACTION_BLUIDER_REQUIRED_KEYS)}.")
        for actionBuilder in self.__actionSpaceBuilders:
            if not all(key in actionBuilder for key in ReinforcementLearning.__ACTION_BLUIDER_REQUIRED_KEYS):
                raise ValueError(f"Missing key in actionSpaceBuilder item. Required keys are: {', '.join(ReinforcementLearning.__ACTION_BLUIDER_REQUIRED_KEYS)}.")
            actionBuilder["step"] = round((actionBuilder["max"] - actionBuilder["min"]) / actionBuilder["intervals"])
        return True

    def getActionsSpace(self) -> List[tuple]:
        """ Returns the space of all actions."""
        actionSpace=[]
        for actionBuilder in self.__actionSpaceBuilders:
            actionSpace=self.__computeCombinations(actionSpace,[v for v in range(-actionBuilder["step"],2*actionBuilder["step"],actionBuilder["step"])])
        actionSpace = [tuple(action) for action in actionSpace]
        return actionSpace

    def getStatesSpace(self) -> List[tuple]:
        """ Returns the space of all states."""
        stateSpace = []
        for stateBuilder in self.__actionSpaceBuilders:
            stateSpace = self.__computeCombinations(stateSpace, [v for v in range(stateBuilder["min"],stateBuilder["max"] + stateBuilder["step"], stateBuilder["step"])])
        stateSpace = [tuple(state) for state in stateSpace]
        return stateSpace

    def __computeCombinations(self,space,value) -> List[list]:
        updatedSpace=[]
        if space:
            for a in space:
                for b in value:
                    na=a.copy()
                    na.append(b)
                    updatedSpace.append(na)
        else:
            for b in value:
                updatedSpace.append([b])
        return updatedSpace

    # GETTERS
    def getReachableStates(self, state:tuple) -> List[tuple]:
        """ Returns all the reachable states for a given state."""
        actionIndices = self.getPossibleActions(state)
        reachableStates = []
        for actionIndex in actionIndices:
            reachableStates.append(self.getNextState(state, actionIndex))
        return reachableStates

    def getNextState(self, state:tuple, actionIndex:int) -> tuple:
        return tuple([self.__actions[actionIndex][i]+state[i] for i in range(len(state))])

    def getPossibleActions(self,state) -> List[int]:
        """ Returns all possibles action for a given state."""
        possibleActionIndexes = [i for i in range(len(self.__actions))]
        for i, action in enumerate(self.__actions):
            for j, actionBuilder in enumerate(self.__actionSpaceBuilders):
                current = state[j]
                if current + action[j] < actionBuilder["min"] or current + action[j] > actionBuilder["max"]:
                    possibleActionIndexes.remove(i)
                    break
        return possibleActionIndexes

    def getActionToExecute(self) -> tuple:
        """ Returns the best action to execute."""
        if self.__actions is None:
            raise ValueError("actionSpaceBuilders have not been given")
        possibleActionsIndexes=self.getPossibleActions(self._state)
        if random.random() < self._explorationRate:
            actionWeights = self.__computeActionWeights(self._state, possibleActionsIndexes)
            self._actionToExecuteIndex=random.choices(population=possibleActionsIndexes,weights=actionWeights,k=1)[0]
        else:
            maxIndex=possibleActionsIndexes[0]
            max=self._QTable[self._state][maxIndex]
            for index in possibleActionsIndexes:
                if self._QTable[self._state][index]>max:
                    max = self._QTable[self._state][index]
                    maxIndex=index
            self._actionToExecuteIndex = maxIndex

        return self.__actions[self._actionToExecuteIndex]

    def __computeActionWeights(self, state:tuple, possibleActionIndexes:List[int]) -> List[float]:
        penalisationFactor = 10
        possibleActionCounts = [(penalisationFactor*self._actionCountTable[state][i]+1) for i in possibleActionIndexes]
        total = sum(possibleActionCounts)
        return [(total-actionCount) / total for actionCount in possibleActionCounts]

    def fillTable(self, tableName: str, initValue: float = 0):
        """ Fills the table passed in parameter with the chosen init value."""
        table = self.__getattribute__(tableName)
        for state in self.getStatesSpace():
            table[state] = [initValue] * len(self.__actions)

    def printTable(self,tableName:str):
        """ Prints the table passed in parameter."""
        table=self.__getattribute__(tableName)
        print(f"----------{tableName}----------")
        for state in table:
            print(state,table[state])
        print("--------------------------------")

    def learn(self,reward:float):
        """ Learns from the executed action.
        @param reward  Reward of the action
        """
        self._explorationRate *= self._factors["explorationRateDecrease"]
        self._learn(reward)
        self._actionCountTable[self._state][self._actionToExecuteIndex]+=1

    def _learnQLearning(self,reward:float):
        """ Executes the chosen action and learn of it (QLearning)
        @param reward  Reward of the action
        """
        nextState=self.getNextState(self._state,self._actionToExecuteIndex)
        maxValue = max(self._QTable[nextState])
        self._QTable[self._state][self._actionToExecuteIndex] = (1 - self._factors["learning"]) * self._QTable[self._state][self._actionToExecuteIndex] + self._factors["learning"] * (reward+self._factors["discount"]*maxValue)
        self._state = nextState

    def _learnValueIteration(self,reward:float):
        """ Executes the chosen action and learn of it (ValueIteration)
        @param reward  Reward of the action
        """
        # Reward update
        actionCount = self._actionCountTable[self._state][self._actionToExecuteIndex]
        oldReward = self._RTable[self._state][self._actionToExecuteIndex]
        self._RTable[self._state][self._actionToExecuteIndex] = (reward+actionCount*oldReward)/(actionCount+1)

        # Value iteration
        for state in self._QTable.keys():
            for actionIndex in self.getPossibleActions(state):
                newState = self.getNextState(state,actionIndex)
                maxValue = max(self._QTable[newState])
                reward = self._RTable[state][actionIndex]
                self._QTable[state][actionIndex]=reward+self._factors["discount"]*maxValue
        self._state = self.getNextState(self._state,self._actionToExecuteIndex)
        self._actionCountTable[self._state][self._actionToExecuteIndex] += 1

    def reset(self):
        self._state=self._initialState

    def loadModel(self,filepath:str):
        """ Loads a JSON pre-trained model."""
        try:
            if filepath.split(".")[-1]!="json":
                raise ValueError("Format of the model invalid (JSON only)")

            with open(filepath) as json_file:
                json_string = json.load(json_file)
                data = json.loads(json_string)
                self.__actionSpaceBuilders=data["actionSpaceBuilders"]
                if self.__areActionBuildersValid():
                    self.__actions=self.getActionsSpace()
                self._QTable = {}
                for key in data["QTable"]:
                    self._QTable[tuple([float(v) for v in key.split(" ")])]=data["QTable"][key]
                if not all(key in self._QTable for key in self.getStatesSpace()):
                    raise ValueError(f"Invalid QTable in model '{filepath}'")
        except FileNotFoundError:
            raise FileNotFoundError(f"Model '{filepath}' not found")

    def saveModel(self, filepath:str= "myModel.json"):
        """ Saves the current trained model in a file. The file must be a JSON file."""
        QTable={}
        for key in self._QTable:
            QTable[" ".join([str(v) for v in key])]=self._QTable[key]

        data = {
            'actionSpaceBuilders': self.__actionSpaceBuilders,
            'QTable':QTable
        }

        json_string = json.dumps(data)
        with open(filepath, 'w') as outfile:
            json.dump(json_string, outfile)

    def updateState(self):
        """ Updates the learning state according to the previous state and the executed action."""
        self._state=self.getNextState(self._state,self._actionToExecuteIndex)