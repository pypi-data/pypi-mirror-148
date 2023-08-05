from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.obstacles import RectangularObstacle
from discoverySimulator.obstacles.CircularObstacle import CircularObstacle
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter


def simpleObstacleAvoidance():
    FORWARD_SPEED = 1000
    TURN_SPEED = 200
    COLLISION_TH = 70

    myRobot = RectangularTwoWheelsRobot()

    telemeters = []

    o=25
    x=20
    y=20

    for i in range(6):
        telemeters.append(Telemeter())
        myRobot.addComponent(telemeters[-1],x,y,o)
        o-=10
        x-=8
        if i<2:
            y+=5
        elif  i>2:
            y-=5

    myEnvironment = Environment(1500,900)
    myEnvironment.addObject(myRobot,500,500,90)
    myEnvironment.addObject(CircularObstacle(50,"#ff0"),800,850)
    myEnvironment.addObject(RectangularObstacle(200,180,"#0ff"),700,530)
    myEnvironment.addObject(CircularObstacle(90,"#f0f"),1000,300)

    mySimulation = Simulation(myEnvironment)
    mySimulation.run()
    mySimulation.showInterface()

    while True:

        if (telemeters[0].getValue()<COLLISION_TH) or (telemeters[1].getValue()<COLLISION_TH) or (telemeters[2].getValue()<COLLISION_TH) and (telemeters[3].getValue()<COLLISION_TH) or (telemeters[4].getValue()<COLLISION_TH) or (telemeters[5].getValue()<COLLISION_TH):
            myRobot.setLeftWheelSpeed(TURN_SPEED)
            myRobot.setRightWheelSpeed(-TURN_SPEED)

        elif (telemeters[0].getValue()<COLLISION_TH) or (telemeters[1].getValue()<COLLISION_TH) or (telemeters[2].getValue()<COLLISION_TH):
            myRobot.setLeftWheelSpeed(-TURN_SPEED)
            myRobot.setRightWheelSpeed(TURN_SPEED)

        elif (telemeters[3].getValue()<COLLISION_TH) or (telemeters[4].getValue()<COLLISION_TH) or (telemeters[5].getValue()<COLLISION_TH):
            myRobot.setLeftWheelSpeed(TURN_SPEED)
            myRobot.setRightWheelSpeed(-TURN_SPEED)

        else:
            myRobot.setLeftWheelSpeed(FORWARD_SPEED)
            myRobot.setRightWheelSpeed(FORWARD_SPEED)

        mySimulation.sync()

