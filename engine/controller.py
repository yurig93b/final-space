import math
import pprint

from celestial_bodies.moon import Moon
from data.sharedstate import SharedState
from simulation.bereshit_simulation import BereshitSimulation
from vehicle.bereshit import BereshitVehicle
import numpy as np


class FlightController(object):
    DT = 0.1

    def __init__(self):
        pass

    @classmethod
    def acc(cls, weight, total_thrust):
        return total_thrust / weight

    def run(self):
        simulator = BereshitSimulation(shared_state=BereshitSimulation.get_initial_state())
        shared_state = simulator.shared_state

        shared_state.dt = self.DT
        vehicle = BereshitVehicle(shared_state)

        while True:
            pprint.pprint(shared_state.__dict__)
            new_state = simulator.step(self.DT, shared_state)
            ang_rad = math.radians(new_state.vehicle_ang)
            h_acc = math.sin(ang_rad) * new_state.acc
            v_acc = math.cos(ang_rad) * new_state.acc
            vacc = Moon.get_acc(new_state.hs)
            new_state.time += self.DT



            MAIN_BURN = 0.15
            SECOND_BURN = 0.009
            ALL_BURN = MAIN_BURN + 8 * SECOND_BURN

            dw = self.DT * ALL_BURN * new_state.thrust #dw = self.DT * vehicle.get_engine_thrust_force() * new_state.thrust
            if new_state.fuel > 0:
                new_state.fuel -= dw
                new_state.weight = vehicle.get_weight(new_state.fuel)
                new_state.acc = new_state.thrust * self.acc(new_state.weight, vehicle.get_engine_thrust_force())
            else:
                new_state.acc = 0
                return np.inf



            v_acc -= vacc
            new_state.hs -= h_acc * self.DT
            new_state.distance -= new_state.hs * self.DT
            new_state.vs -= v_acc * self.DT
            new_state.alt -= self.DT * new_state.vs

            shared_state = new_state


