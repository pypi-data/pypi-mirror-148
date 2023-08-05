from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.actuators import LED


def blinkWithoutSleep():
    myLED = LED()

    myEnvironment = Environment(500, 500)
    myEnvironment.addObject(myLED, myEnvironment.getWidth() / 2, myEnvironment.getHeight() / 2)

    mySimulation = Simulation(myEnvironment)
    mySimulation.showInterface()
    mySimulation.run()

    startTime = mySimulation.time()

    while True:
        currentTime = mySimulation.time()
        if currentTime - startTime >= 1:
            startTime = currentTime
            myLED.toggleState()

        mySimulation.sync()
