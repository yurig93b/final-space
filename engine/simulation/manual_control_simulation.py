import copy
import time

from data.sharedstate import SharedState
from pid.pid import PID
from simulation.base_simulation import BaseSimulation
from simulation.fts_activated import FtsActivatedException
from simulation.simulation_ended import SimulationEnded


class ManualControlSimulation(BaseSimulation):
    MIN_ANG = -15
    MAX_ANG = 15

    def __init__(self, shared_state: SharedState):
        super().__init__(shared_state)
        self.pid_ang = PID(0.5, 0.05, 0.01, 3)


    def step(self, dt, current_state: SharedState) -> SharedState:
        error_wanted_ang = current_state.vehicle_ang - current_state.wanted_vehicle_ang
        pid_error_ang = self.pid_ang.update(error_wanted_ang, dt)

        ret_state: SharedState = copy.deepcopy(current_state)
        ret_state.vehicle_ang = PID.constrain(current_state.vehicle_ang - pid_error_ang, self.MIN_ANG, self.MAX_ANG)
        ret_state.thrust = current_state.wanted_thrust
        return ret_state

    @classmethod
    def get_initial_state(cls) -> SharedState:
        s = SharedState()
        s.vs = 0
        s.hs = 0
        s.distance = 0
        s.alt = 0
        s.fuel = 200
        s.wanted_thrust = 0


        return s
