import copy
import math
import pprint

import matplotlib.pyplot as plt
import socketio

from celestial_bodies.moon import Moon
from data.sharedstate import SharedState
from simulation.bereshit_simulation import BereshitSimulation
from simulation.fts_activated import FtsActivatedException
from simulation.manual_control_simulation import ManualControlSimulation
from simulation.simulation_ended import SimulationEnded
from simulation.starhoper_simulation import StarhoperSimulation
from vehicle.bereshit import BereshitVehicle


class FlightController(socketio.ClientNamespace):
    DT = 0.1

    def __init__(self, namespace=None):
        super().__init__(namespace)
        self._current_simulation = None
        self._shared_state:SharedState = None

    def on_connect(self):
        pass

    def on_disconnect(self):
        pass

    def on_start_simulation(self, data):
        self.run_simulation(data)

    def on_new_control_info(self, data):
        print('**********************************************')
        print(f'data = {data}')
        print('**********************************************')
        self._shared_state.wanted_thrust = float(data.get('wanted_thrust', 0.0))
        self._shared_state.wanted_vehicle_ang = float(data.get('wanted_vehicle_ang', 0.0))

    @classmethod
    def acc(cls, weight, total_thrust):
        return total_thrust / weight

    def emit_error(self, msg):
        self.emit("err_server", msg)

    def run_simulation(self, simulation):
        if self._current_simulation:
            self.emit_error("A simulation is already running.")
            return

        if simulation == "bereshit":
            self._current_simulation = BereshitSimulation(shared_state=BereshitSimulation.get_initial_state())
        elif simulation == "starhoper":
            self._current_simulation = StarhoperSimulation(shared_state=StarhoperSimulation.get_initial_state())
        elif simulation == "manual_control":
            self._current_simulation = ManualControlSimulation(shared_state=ManualControlSimulation.get_initial_state())
        else:
            self.emit_error("Unknown simulation")

        self.emit("simulation_started")
        self._shared_state = self._current_simulation.shared_state
        self._shared_state.dt = self.DT
        vehicle = BereshitVehicle(self._shared_state)

        p_d = []

        try:
            while True:
                pprint.pprint(self._shared_state.__dict__)
                new_state = self._current_simulation.step(self.DT, self._shared_state)
                ang_rad = math.radians(new_state.vehicle_ang)
                h_acc = math.sin(ang_rad) * new_state.acc
                v_acc = math.cos(ang_rad) * new_state.acc
                vehicle_acc = Moon.get_acc(new_state.hs)
                new_state.time += self.DT

                dw = self.DT * vehicle.get_engine_fuel_burn_rate_per_second() * new_state.thrust
                if new_state.fuel > 0:
                    new_state.fuel -= dw
                    new_state.weight = vehicle.get_weight(new_state.fuel)
                    new_state.acc = new_state.thrust * self.acc(new_state.weight, vehicle.get_engine_thrust_force())
                else:
                    new_state.acc = 0
                    break

                v_acc -= vehicle_acc
                new_state.hs -= h_acc * self.DT
                new_state.distance -= new_state.hs * self.DT
                new_state.vs -= v_acc * self.DT
                new_state.alt -= self.DT * new_state.vs
                new_state.alt = max(new_state.alt, 0)
                new_state.ang_relative_to_body = new_state.ang_relative_to_body + \
                                                 (self._shared_state.hs * self._shared_state.dt) / (
                                                             Moon.get_radius() + new_state.alt)

                self._shared_state = new_state
                self.emit("flight_status", self._shared_state.__dict__)
                p_d.append(copy.deepcopy(new_state))

        except SimulationEnded:
            self.emit("simulation_ended", self._shared_state.__dict__)
        except FtsActivatedException:
            self.emit("fts_activated", self._shared_state.__dict__)
        except Exception as e:
            self.emit("err_server", e.__repr__())
            raise e
        finally:
            self._current_simulation = None
            self._shared_state = None

            fig, axs = plt.subplots(8, 1, constrained_layout=True)
            axs[0].plot([s.time for s in p_d], [s.alt for s in p_d])
            axs[0].set_xlabel('time')
            axs[0].set_ylabel('alt')

            axs[1].plot([s.time for s in p_d], [s.vs for s in p_d])
            axs[1].set_xlabel('time')
            axs[1].set_ylabel('vs')

            axs[2].plot([s.time for s in p_d], [s.wanted_vs for s in p_d])
            axs[2].set_xlabel('time')
            axs[2].set_ylabel('wanted_vs')

            axs[3].plot([s.time for s in p_d], [s.thrust for s in p_d])
            axs[3].set_xlabel('time')
            axs[3].set_ylabel('thrust')

            axs[4].plot([s.time for s in p_d], [s.hs for s in p_d])
            axs[4].set_xlabel('time')
            axs[4].set_ylabel('hs')

            axs[5].plot([s.time for s in p_d], [s.vehicle_ang for s in p_d])
            axs[5].set_xlabel('time')
            axs[5].set_ylabel('ang')

            axs[6].plot([s.time for s in p_d], [s.acc for s in p_d])
            axs[6].set_xlabel('time')
            axs[6].set_ylabel('acc')

            axs[7].plot([s.time for s in p_d], [s.fuel for s in p_d])
            axs[7].set_xlabel('time')
            axs[7].set_ylabel('fuel')
            #
            # plt.xlabel('t')
            # plt.ylabel('alt')
            #plt.show()

    def run(self):
        self.run_simulation("manual_control")
