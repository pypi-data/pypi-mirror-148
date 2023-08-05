from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.tools.learning import ReinforcementLearning

from discoverySimulator.config import *


# In this example, a robot will learn to go forward. The training can be imperfect due to the non-perfect
# synchronisation of the user code and the simulation refresh.
def useOfReinforcementLearningToLearn():
    myEnvironment = Environment(1000, 800)
    myRobot = RectangularTwoWheelsRobot()
    myRobot.enableOdometry()
    myEnvironment.addObject(myRobot, 50, 400, -90)

    mySimulation = Simulation(myEnvironment)
    mySimulation.run()
    mySimulation.showInterface()

    initialPose = myRobot.getPose().copy()
    currentState = (myRobot.getLeftWheel().getSpeed(), myRobot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState, [
        {"min": 0, "max": 800, "intervals": 2},  # Left wheel
        {"min": 0, "max": 800, "intervals": 2}  # Right wheel
    ])

    EPISODE_TIME_LEARNING = 6
    TOTAL_TIME_LEARNING = 420
    start = mySimulation.time()

    while mySimulation.time() < TOTAL_TIME_LEARNING:

        current = mySimulation.time()
        if current - start < EPISODE_TIME_LEARNING:
            startPosition = (myRobot.getPose().getX(), myRobot.getPose().getY())
            startOrientation = myRobot.getPose().getOrientation()
            startOrientation %= 360

            # Action during 0.2 second to see the result of the action
            action = reinforcementLearning.getActionToExecute()
            myRobot.setRightWheelSpeed(myRobot.getRightWheel().getSpeed() + action[0])
            myRobot.setLeftWheelSpeed(myRobot.getLeftWheel().getSpeed() + action[1])

            mySimulation.sleep(0.1)
            mySimulation.sync()

            endPosition = (myRobot.getPose().getX(), myRobot.getPose().getY())
            endOrientation = myRobot.getPose().getOrientation()

            distance = ((endPosition[0] - startPosition[0]) ** 2 + (endPosition[1] - startPosition[1]) ** 2) ** .5

            reward = distance / (1 + (endOrientation - startOrientation) ** 2)  # Encourages going straight
            reinforcementLearning.learn(reward)
        else:
            start = mySimulation.time()
            myRobot.setPose(initialPose.copy())
            myRobot.setLeftWheelSpeed(0)
            myRobot.setRightWheelSpeed(0)
            myRobot.setCollidedState(False)
            reinforcementLearning.reset()
        mySimulation.sync()

    myRobot.stop()
    mySimulation.stop()
    reinforcementLearning.saveModel("goForwardTwoWheelsRobotModel.json")


def useOfReinforcementLearningFromModel():
    myEnvironment = Environment(800, 800)
    myRobot = RectangularTwoWheelsRobot()
    myEnvironment.addObject(myRobot, 50, 400, -90)

    mySimulation = Simulation(myEnvironment)
    mySimulation.run()
    mySimulation.showInterface()

    currentState = (myRobot.getLeftWheel().getSpeed(), myRobot.getRightWheel().getSpeed())
    reinforcementLearning = ReinforcementLearning(currentState)
    reinforcementLearning.loadModel(
        os.path.join(path, "ressources", "pretrainedRLModels", "goForwardTwoWheelsRobotModel.json"))

    while True:
        action = reinforcementLearning.getActionToExecute()
        myRobot.setRightWheelSpeed(myRobot.getRightWheel().getSpeed() + action[0])
        myRobot.setLeftWheelSpeed(myRobot.getLeftWheel().getSpeed() + action[1])
        reinforcementLearning.updateState()
        mySimulation.sync()
