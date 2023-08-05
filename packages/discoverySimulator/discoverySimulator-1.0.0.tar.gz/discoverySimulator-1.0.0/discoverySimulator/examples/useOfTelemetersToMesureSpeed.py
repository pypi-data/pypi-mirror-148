from discoverySimulator.robots import FourWheelsRobot
from discoverySimulator.sensors import Telemeter
from discoverySimulator.simulation import Environment, Simulation


def useOfTelemetersToMesureSpeed():
    environmentWidth = 800
    environmentHeight = 400
    myEnvironment=Environment(environmentWidth,environmentHeight)

    myRobot = FourWheelsRobot()
    myEnvironment.addObject(myRobot,150,environmentHeight/2,-90)
    myRobot.setRightWheelSpeed(200)
    myRobot.setLeftWheelSpeed(200)

    offset = 4
    myTelemeter1=Telemeter()
    positionTelemeter1=300
    myEnvironment.addObject(myTelemeter1,positionTelemeter1,offset)
    myTelemeter2=Telemeter()
    positionTelemeter2=500
    myEnvironment.addObject(myTelemeter2,positionTelemeter2,offset)

    mySimulation = Simulation(myEnvironment)
    mySimulation.run()
    mySimulation.showInterface()

    distance = positionTelemeter2-positionTelemeter1
    firstTime = 0
    clock = 0
    counter = 0 # State machine


    while True :

        if myTelemeter1.getValue()<environmentHeight*3/4 and counter == 0:
            firstTime=mySimulation.time()
            counter+=1
            print(f"First detection time: {firstTime}s")

        elif myTelemeter2.getValue()<environmentHeight*3/4 and counter == 1:
            secondTime=mySimulation.time()
            counter+=1
            print(f"Second detection time: {secondTime}s")
            clock = secondTime - firstTime

        elif counter == 2:
            speed = distance/clock
            counter+=1
            print(f"Speed: {speed}px/s")
            mySimulation.sleep(5)
            myRobot.stop()

        mySimulation.sync()





