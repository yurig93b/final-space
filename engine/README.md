The python engine commmunicates with the UI via a message broker based on Socket.IO.

The simulations are created by implementing a BaseSimulator class and a step class.
The following simulation were implemented:
1. Starhoper simulation - Go up and down a couple time then reach an apogee of 1KM for a couople of seconds, hold it and then land safely.
2. Bereshit simulation - with 3 PID controller (ang, hs and vs). 
3. Manual simulation - to control the simulation with input from the UI.

On a good landing (withing thresholds) a "SimulationEnded" exception is raised. If the simulator detects and unrecoverable state it will throw a "FtsActivatedException" meaning we have activated flight termination (boom).

The main flight controller is implemented in the controller.py file.

Disregard landing.py as it is the original file we were based on before reconstructing everything.
To run please install requierments.txt and run main.py (after running the WS server).
