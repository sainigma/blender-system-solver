## Description
This is a simple system equation solver for accelerating systems. The system receives a case object that contains:
* **spatialObject** that contains the current position, velocity and acceleration of the system
* **acceleration()**, function that defines the system
* **endConditionReached()**, function that defines when the simulation stops

To run, execute **solveAcceleratingSystem()** and provide it with:
* The system object
* Function for outputting the system, for example a function that prints the state
* Interval for executing the previosly mentioned function

I'll add a blender implementation for this code when I finish some examples for different systems.