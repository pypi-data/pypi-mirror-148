from discoverySimulator.simulation import Environment, Simulation
from discoverySimulator.robots import CircularTwoWheelsRobot
from discoverySimulator.obstacles import CircularObstacle, RectangularObstacle, Obstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes import Polygon
from discoverySimulator.tools.path import PathFinding, PathFollowing


def useOfPathFinding():
    myRobot = CircularTwoWheelsRobot()

    myEnvironment = Environment(800,800)
    mySimulation = Simulation(myEnvironment)

    myEnvironment.addObject(myRobot,70,70,-90)
    myEnvironment.addObject(CircularObstacle(70,"#33FF9E"),650,200)
    myEnvironment.addObject(CircularObstacle(50,"#F8FF00"),100,280)
    myEnvironment.addObject(CircularObstacle(100,"#FF8700"),220,620)
    myEnvironment.addObject(RectangularObstacle(400,30,"#FF33F7"),202,200)
    myEnvironment.addObject(Obstacle(Representation(Polygon([(500,200),(800,200),(600,300)],"#BDB9E6"))),-86,234)

    mySimulation.run()
    mySimulation.showInterface()

    mySimulation.sleep(2) # Wait before starting to find the path

    pathFinding = PathFinding(myEnvironment,myRobot.getBoundingWidth(),True,0)
    pathFollowing = PathFollowing(myRobot)

    pathFinding.findPath((myRobot.getPose().getX(),myRobot.getPose().getY()),(700,550),pathFollowing.startFollowing)