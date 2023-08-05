from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.actuators import LED


def blink():
    myLED = LED()

    myEnvironment = Environment(500, 500)
    myEnvironment.addObject(myLED, myEnvironment.getWidth() / 2, myEnvironment.getHeight() / 2)

    mySimulation = Simulation(myEnvironment)
    mySimulation.showInterface()
    mySimulation.run()

    while True:
        myLED.toggleState()
        mySimulation.sleep(1)

        mySimulation.sync()
