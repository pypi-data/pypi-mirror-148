from discoverySimulator import Object
from discoverySimulator.representation import Representation
from discoverySimulator.simulation import Environment, Simulation

from discoverySimulator.representation.shapes import Polygon
from discoverySimulator.robots import RectangularTwoWheelsRobot
from discoverySimulator.sensors import ColorSensor

# Be careful when using a too high acceleration of the simulation. The robot don't have the time to correct its
# trajectory because the delay between two refreshment of the value of its sensors is too high in comparaison with
# the instantaneous movement of the robot.
def roadFollowing():
    myRobot = RectangularTwoWheelsRobot()

    FORWARD_SPEED = 300
    TURN_SPEED = 100
    ROAD_COLOR = "#444444"

    colorSensorRight = ColorSensor()
    colorSensorLeft = ColorSensor()

    myRobot.addComponent(colorSensorRight, 5, 25)
    myRobot.addComponent(colorSensorLeft, -5, 25)

    myEnvironment = Environment(1200, 800)
    polygon = Polygon(
        [(200, 500), (300, 450), (350, 300), (450, 250), (550, 330), (800, 150), (900, 160), (950, 220), (900, 400),
         (860, 430), (780, 420), (720, 450), (640, 560), (550, 610), (400, 560), (250, 620), (200, 580)], ROAD_COLOR)

    myEnvironment.addVirtualObject(Object(Representation(polygon)))
    polygonOffset = polygon.offset(-30)
    polygonOffset.setColor("#f0f0f0")
    myEnvironment.addVirtualObject(Object(Representation(polygonOffset)), polygonOffset.getPose().getX(),
                                   polygonOffset.getPose().getY())

    myEnvironment.addObject(myRobot, 250, 480)

    mySimulation = Simulation(myEnvironment)
    mySimulation.run()
    mySimulation.showInterface()

    while True:
        if colorSensorRight.getValue() == ROAD_COLOR and colorSensorLeft.getValue() == ROAD_COLOR: # On the path
            myRobot.setLeftWheelSpeed(FORWARD_SPEED)
            myRobot.setRightWheelSpeed(FORWARD_SPEED)
        elif colorSensorRight.getValue() != ROAD_COLOR and colorSensorLeft.getValue() == ROAD_COLOR: # On the right side of the path
            myRobot.setLeftWheelSpeed(-TURN_SPEED)
            myRobot.setRightWheelSpeed(TURN_SPEED)
        elif colorSensorRight.getValue() == ROAD_COLOR and colorSensorLeft.getValue() != ROAD_COLOR: # On the left side of the path
            myRobot.setLeftWheelSpeed(TURN_SPEED)
            myRobot.setRightWheelSpeed(-TURN_SPEED)
        else:
            # Outside the path
            myRobot.stop()

        mySimulation.sync()
