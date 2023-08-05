# Robotic simulator for Python

## What's this
**discoverySimulator** is a Python package allowing to simulate environments in which mobile robots evolve. This simulator is accompanied by an interface allowing to visualize and control the simulation. This package is ideal for a playful learning of python and a discovery of mobile robotics.

## Documentation
The documentation associated with this python package can be found [here](https://discoverysimulator.github.io/).

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the package  **discoverySimulator**:

```bash
$ pip install discoverySimulator
```

## Usage example

### Code
```python
from discoverySimulator.simulation import Simulation, Environment
from discoverySimulator.robots import RectangularTwoWheelsRobot

# Create robot and assign wheel speed
myRobot = RectangularTwoWheelsRobot()
myRobot.setRightWheelSpeed(500)
myRobot.setLeftWheelSpeed(200)

# Create environment
environmentWidth = 1500
environmentHeight = 1500
myEnvironment = Environment(environmentWidth,environmentHeight)
myEnvironment.addObject(myRobot,200,200,90)

# Create and run simulation 
mySimulation = Simulation(myEnvironment)
mySimulation.run()
mySimulation.showInterface()
```
### Code result 
![screenshot](https://github.com/discoverySimulator/discoverySimulatorPythonPackage/blob/main/code_result.png?raw=true)

## Help and bug reports
General questions and comments can be sent to the following email address: [discoverysimulator@gmail.com](mailto:discoverysimulator@gmail.com).

You can also report bugs at this same email address.

## How to contribute
We are open to contributions, so send us your ideas or code amendments to the following email address: [discoverysimulator@gmail.com](mailto:discoverysimulator@gmail.com), and we will do our best to accommodate you!

## Credits
Copyright (c) 2022, Leo Planquette & Eloise Lefebvre.

## License
**discoverySimulator** is released under the GPL v3 license and under a commercial license that allows for the development of proprietary applications.

Additional details about this license can be found [here](https://choosealicense.com/licenses/gpl-3.0/).
