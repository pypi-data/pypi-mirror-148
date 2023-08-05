from discoverySimulator.simulation import Environment, Simulation

from discoverySimulator.robots.RectangularTwoWheelsRobot import RectangularTwoWheelsRobot
from discoverySimulator.sensors import LIDAR

from discoverySimulator.obstacles import Obstacle, CircularObstacle, RectangularObstacle
from discoverySimulator.representation import Representation
from discoverySimulator.representation.shapes.Polygon import Polygon


def useOfLIDAR():
    lidar = LIDAR()
    rob = RectangularTwoWheelsRobot()
    rob.addComponent(lidar)
    rob.setRightWheelSpeed(200)
    rob.setLeftWheelSpeed(400)

    env = Environment(1500, 900)
    env.addObject(rob, 900, 500)
    env.addObject(CircularObstacle(40, "#ff8fff"), 150, 180)
    env.addObject(RectangularObstacle(40, 200, "#ff8fff"), 500, 200,45)
    env.addObject(RectangularObstacle(400, 100, "#ff8fff"), 250, 750, 25)
    pol=Polygon([(900,300),(1000,200),(1200,200),(1100,300),(1100,400),(1000,400)],"#ff8fff")
    env.addObject(Obstacle(Representation(pol)))

    sim = Simulation(env)
    sim.run()
    sim.showInterface()