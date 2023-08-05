from setuptools import find_packages, setup


def readme():
    with open("README.md") as f:
        return f.read()


setup(
    name="discoverySimulator",
    version="1.0.0",
    description="discoverySimulator is a Python package allowing to simulate environments in which mobile robots evolve. This simulator is accompanied by an interface allowing to visualize and control the simulation. This package is ideal for a playful learning of python and a discovery of mobile robotics.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="robot robotic python students simulator education teaching",

    packages=find_packages(),
    install_requires=["PyQt5"],

    author="Leo Planquette & Eloise Lefebvre",
    author_email="discoverysimulator@gmail.com",
    url="https://github.com/discoverySimulator/discoverySimulatorPythonPackage",
    package_data={
        '': ['*.svg']
    },
    include_package_data=True,
    license="GPL v3",
    license_files = ('LICENSE',),
    zip_safe=False
)
