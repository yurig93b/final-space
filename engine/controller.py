import math
import pprint

from celestial_bodies.moon import Moon
from data.sharedstate import SharedState
from simulation.bereshit_simulation import BereshitSimulation
from simulation.fts_activated import FtsActivatedException
from simulation.simulation_ended import SimulationEnded
from vehicle.bereshit import BereshitVehicle
import numpy as np
import socketio


class FlightController(socketio.ClientNamespace):
    DT = 0.1

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_start_simulation(self, data):
        pass


    @classmethod
    def acc(cls, weight, total_thrust):
        return total_thrust / weight

    def run(self):
        self.emit("flight_controller_start")

        simulator = BereshitSimulation(shared_state=BereshitSimulation.get_initial_state())
        shared_state = simulator.shared_state

        shared_state.dt = self.DT
        vehicle = BereshitVehicle(shared_state)

        try:
            while True:
                pprint.pprint(shared_state.ang_relative_to_body)
                new_state = simulator.step(self.DT, shared_state)
                ang_rad = math.radians(new_state.vehicle_ang)
                h_acc = math.sin(ang_rad) * new_state.acc
                v_acc = math.cos(ang_rad) * new_state.acc
                vacc = Moon.get_acc(new_state.hs)
                new_state.time += self.DT

                dw = self.DT * vehicle.get_engine_fuel_burn_rate_per_second() * new_state.thrust
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
                new_state.ang_relative_to_body =  new_state.ang_relative_to_body + \
                                                  (shared_state.hs * shared_state.dt)/(Moon.get_radius() + new_state.alt)

                shared_state = new_state
                self.emit("flight_status", shared_state.__dict__)

        except SimulationEnded:
            self.emit("simulation_ended", shared_state.__dict__)
        except FtsActivatedException:
            self.emit("fts_activated", shared_state.__dict__)
        except Exception as e:
            self.emit("err_server", e)



