from discoverySimulator.simulation import Simulation, Environment
from discoverySimulator import Object
from discoverySimulator.actuators import LED
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Rectangle, Line
from discoverySimulator.robots import FourWheelsRobot, RectangularTwoWheelsRobot
from discoverySimulator.sensors import Telemeter


def parkingScenario():
    environmentWidth = 600
    environmentHeight = 700
    myEnvironment = Environment(environmentWidth, environmentHeight)

    myRobot = FourWheelsRobot()
    myEnvironment.addObject(myRobot, environmentWidth/2, 250, -90)
    myRobot2 = RectangularTwoWheelsRobot()
    myEnvironment.addObject(myRobot2, environmentWidth-50, 350, -90)
    floor = Object(Representation(Rectangle(environmentWidth, environmentHeight, "#444")))
    myEnvironment.addVirtualObject(floor, environmentWidth / 2, environmentHeight / 2)

    telemeters = []
    redLeds = []
    greenLeds = []

    for i in range(4):
        myEnvironment.addVirtualObject(Object(Representation(Line(100, 4, "#fff"))), environmentWidth - 100, 200 + i * 100, -90)

    for i in range(3):
        telemeters.append(Telemeter("#f00", 96))
        myEnvironment.addObject(telemeters[i], environmentWidth - 4, 250 + i * 100, 90)

        redLeds.append(LED(LED.RED))
        myEnvironment.addObject(redLeds[i], environmentWidth + 10, 233 + i * 100)

        greenLeds.append(LED(LED.GREEN))
        myEnvironment.addObject(greenLeds[i], environmentWidth + 10, 263 + i * 100)

    sim = Simulation(myEnvironment)
    sim.showInterface()
    sim.run()

    while True:
        for i in range(3):
            if telemeters[i].getValue() < telemeters[i].getMaximumMeasurableDistance()/2:
                redLeds[i].setState(LED.HIGH)
                greenLeds[i].setState(LED.LOW)
            else:
                greenLeds[i].setState(LED.HIGH)
                redLeds[i].setState(LED.LOW)

        sim.sync()
