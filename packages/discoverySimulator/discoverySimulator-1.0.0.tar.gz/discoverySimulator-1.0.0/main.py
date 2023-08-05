from discoverySimulator.simulation import Simulation, Environment
from discoverySimulator.robots import RectangularTwoWheelsRobot

# Create robot and assign wheel speed
myRobot = RectangularTwoWheelsRobot()
myRobot.setRightWheelSpeed(500)
myRobot.setLeftWheelSpeed(200)

# Create environment
environmentWidth = 800
environmentHeight = 800
myEnvironment = Environment(environmentWidth,environmentHeight)
myEnvironment.addObject(myRobot,300,300,90)

# Create and run simulation
mySimulation = Simulation(myEnvironment)
mySimulation.run()
mySimulation.showInterface()

# from discoverySimulator.demonstrations import scenario
# scenario()

from discoverySimulator.examples import blinkWithoutSleep, useOfLIDAR, roadFollowing, useOfPathFinding, useOfReinforcementLearningToLearn, \
useOfReinforcementLearningFromModel, parkingScenario, fuzzyLogicObstacleAvoidance, simpleObstacleAvoidance, robotMovement, useOfTelemetersToMesureSpeed
# useOfLIDAR()
# roadFollowing()
# blinkWithoutSleep()
# useOfPathFinding()
# useOfReinforcementLearningToLearn()
# useOfReinforcementLearningFromModel()
# parkingScenario()
# fuzzyLogicObstacleAvoidance()
# simpleObstacleAvoidance()
# robotMovement()

# useOfTelemetersToMesureSpeed()
#
# from discoverySimulator.tests import aStar, collisionAndTelemeter, usingLIDAR, reinforcementLearning, \
#     road, measureSpeedWithTelemeters

# reinforcementLearning.reinforcementLearningFromModel()
# aStar()
# collisionAndTelemeter()
# usingLIDAR.LIDARTest()
# # reinforcementLearningTest()
# # rlTwoWheelsRobot.reinforcementLearningTest()
# # rlAvoiding.reinforcementLearningTest()
# road.road()
# measureSpeedWithTelemeters.measureSpeedWithTelemeters()
