from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.tools.maps import Maze
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter

def fuzzyLogicObstacleAvoidance():
    FORWARD_SPEED = 500

    myRobot = RectangularTwoWheelsRobot()

    leftFrontTelemeter = Telemeter('#dd9999')  # Front left telemeter
    rightFrontTelemeter = Telemeter('#dd9999')  # Front right telemeter
    rightTelemeter = Telemeter('#dd9999')
    leftTelemeter = Telemeter('#dd9999')
    myRobot.addComponent(leftFrontTelemeter, -20, 30, -10)
    myRobot.addComponent(rightFrontTelemeter, 20, 30, 10)
    myRobot.addComponent(leftTelemeter, -20, 20, -35)
    myRobot.addComponent(rightTelemeter, 20, 20, 35)

    distantObstacle = []
    rightTurnRightWheel = [0 for _ in range(11)]
    rightTurnLeftWheel = [0 for _ in range(11)]
    leftTurnRightWheel = [0 for _ in range(11)]
    leftTurnLeftWheel = [0 for _ in range(11)]

    for i in range(50):
        distantObstacle.append(0)
    for i in range(50, 300):
        distantObstacle.append(i * 5 - 250)
    for i in range(300, leftTelemeter.getMaximumMeasurableDistance() + 1):
        distantObstacle.append(100)

    for i in range(-5, 6):
        if i < 0:
            rightTurnRightWheel[i + 5] = (-20 * i)
        else:
            rightTurnRightWheel[i + 5] = 0
        leftTurnLeftWheel[i + 5] = rightTurnRightWheel[i + 5]
    for i in range(-5, 6):
        if i < 0:
            rightTurnLeftWheel[i + 5] = (20 * i)
        else:
            rightTurnRightWheel[i + 5] = 0
        leftTurnRightWheel[i + 5] = rightTurnLeftWheel[i + 5]

    myEnvironment = Environment(1500, 1500)
    myEnvironment.addObject(myRobot, 1000, 500, 20)

    mySimulation = Simulation(myEnvironment)
    myMaze = Maze(myEnvironment)
    myMaze.draw()

    mySimulation.run()
    mySimulation.showInterface()

    myRobot.setRightWheelSpeed(FORWARD_SPEED)
    myRobot.setLeftWheelSpeed(FORWARD_SPEED)

    while True:

        distantObstacleLeftFrontTelemeter = distantObstacle[int(leftFrontTelemeter.getValue())]
        distantObstacleRightFrontTelemeter = distantObstacle[int(rightFrontTelemeter.getValue())]
        distantObstacleRightSensor = distantObstacle[int(rightTelemeter.getValue())]
        distantObstacleLeftSensor = distantObstacle[int(leftTelemeter.getValue())]

        numerator = 0
        denominator = 0

        # Right wheel
        for x in range(11):
            cutValueLeftFrontTelemeter = min(distantObstacleLeftFrontTelemeter, rightTurnRightWheel[x])
            cutValueRightFrontTelemeter = min(distantObstacleRightFrontTelemeter, leftTurnRightWheel[x])
            cutValueRightSensor = min(distantObstacleRightSensor, leftTurnRightWheel[x])
            cutValueLeftSensor = min(distantObstacleLeftSensor, rightTurnRightWheel[x])

            numerator += (x - 5) * (
                        cutValueLeftFrontTelemeter + cutValueRightFrontTelemeter + cutValueRightSensor + cutValueLeftSensor)
            denominator += (
                        cutValueLeftFrontTelemeter + cutValueRightFrontTelemeter + cutValueRightSensor + cutValueLeftSensor)

        if denominator != 0:
            gravity = numerator / denominator
        else:
            gravity = 100
        myRobot.setRightWheelSpeed(gravity)

        numerator = 0
        denominator = 0

        # Left wheel
        for x in range(11):
            cutValueLeftFrontTelemeter = min(distantObstacleLeftFrontTelemeter, rightTurnLeftWheel[x])
            cutValueRightFrontTelemeter = min(distantObstacleRightFrontTelemeter, leftTurnLeftWheel[x])
            cutValueRightSensor = min(distantObstacleRightSensor, leftTurnLeftWheel[x])
            cutValueLeftSensor = min(distantObstacleLeftSensor, rightTurnLeftWheel[x])

            numerator += (x - 5) * (
                        cutValueLeftFrontTelemeter + cutValueRightFrontTelemeter + cutValueRightSensor + cutValueLeftSensor)
            denominator += (
                        cutValueLeftFrontTelemeter + cutValueRightFrontTelemeter + cutValueRightSensor + cutValueLeftSensor)

        if denominator != 0:
            gravity = numerator / denominator
        else:
            gravity = 100
        myRobot.setLeftWheelSpeed(gravity)

        mySimulation.sync()
