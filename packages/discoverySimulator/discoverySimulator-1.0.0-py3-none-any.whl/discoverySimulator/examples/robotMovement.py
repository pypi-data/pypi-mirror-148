from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.obstacles.CircularObstacle import CircularObstacle
from discoverySimulator.robots import RectangularTwoWheelsRobot, FourWheelsRobot, CircularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.actuators import LED


def robotMovement():
    myRobot1 = RectangularTwoWheelsRobot()
    myRobot1.setRightWheelSpeed(200)
    myRobot1.setLeftWheelSpeed(200)

    myLED1 = LED(LED.RED)
    myLED2 = LED(LED.YELLOW)
    myLED3 = LED(LED.BLUE)
    myLED4 = LED(LED.YELLOW)

    myRobot1.addComponent(myLED1, 0, -10)
    myRobot1.addComponent(myLED2, 0, 10)

    myRobot2 = CircularTwoWheelsRobot()
    myRobot2.addComponent(myLED3, 0, 0)
    myRobot2.setRightWheelSpeed(100)
    myRobot2.setLeftWheelSpeed(200)

    myRobot2.enableOdometry()

    myTelemeter = Telemeter()
    myTelemeter.setID("Front_Telemeter")
    myRobot3 = RectangularTwoWheelsRobot()
    myRobot3.addComponent(myTelemeter, 0, 25, 0)

    myRobot3.setLeftWheelSpeed(200)
    myRobot3.setRightWheelSpeed(-200)

    myRobot4 = FourWheelsRobot("#f00")
    myRobot4.addComponent(myLED4, 0, 0)
    myRobot4.setBackRightWheelSpeed(300)
    myRobot4.setFrontRightWheelSpeed(300)
    myRobot4.setBackLeftWheelSpeed(500)
    myRobot4.setFrontLeftWheelSpeed(-300)

    myRobot5 = RectangularTwoWheelsRobot()
    myRobot5.setRightWheelSpeed(300)
    myRobot5.setLeftWheelSpeed(300)

    myEnvironment = Environment(1500, 900)
    myEnvironment.addObject(myRobot1, 1000, 100, 30)
    myEnvironment.addObject(myRobot2, 1050, 300, -45)
    myEnvironment.addObject(myRobot3, 500, 500, 45)
    myEnvironment.addObject(myRobot4, 700, 500, 90)
    myEnvironment.addObject(myRobot5, 700, 180, 90)
    myEnvironment.addObject(CircularObstacle(40, "#ff8fff"), 150, 180)

    mySimulation = Simulation(myEnvironment)
    ledState = 0
    mySimulation.run()
    mySimulation.showInterface()

    while True:
        ledState = not ledState
        myLED1.setState(ledState)
        myLED2.setState(not ledState)
        myLED3.setState(ledState)
        myLED4.setState(ledState)
        mySimulation.sleep(1)

        mySimulation.sync()
