The python engine commmunicates with the UI via a message broker based on Socket.IO.

The simulations are created by implementing a BaseSimulator class and a step class.
The following simulation were implemented:
1. Starhoper simulation - Go up and down a couple time then reach an apogee of 1KM for a couople of seconds, hold it and then land safely.
2. Bereshit simulation - with 3 PID controller (ang, hs and vs). 
3. Manual simulation - to control the simulation with input from the UI.

The moon was implemented as a "celestial body" class with its own paramters for an easy change in the future.

The vehicle was implemneted as a "vehicle" class with its own parameters.

How is the vehicle position calculated and transferred in a simulation?
We take the current hs and altitude and treat the vehicle in a position of a circle with radius=radius_of_moon+altitude. We then calculcate how many degress of angle are added if we travel in the circumference of the new circle in the speed we currently have. The angle is integrated between steps.

On a good landing (withing thresholds) a "SimulationEnded" exception is raised. If the simulator detects and unrecoverable state it will throw a "FtsActivatedException" meaning we have activated flight termination (boom).

The main flight controller is implemented in the controller.py file.

Disregard landing.py as it is the original file we were based on before reconstructing everything.
To run please install requierments.txt and run main.py (after running the WS server).
