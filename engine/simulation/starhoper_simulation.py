import copy
import time

from data.sharedstate import SharedState
from pid.pid import PID
from simulation.base_simulation import BaseSimulation
from simulation.fts_activated import FtsActivatedException
from simulation.simulation_ended import SimulationEnded


class StarhoperSimulation(BaseSimulation):
    STATE_ASCENDING = 0
    STATE_APOGEE = 1
    STATE_DESCENDING = 2

    TARGET_VS = 10
    TARGET_HS = 10
    MIN_ANG = -3
    MAX_ANG = 3

    INTEGRAL_VS_PID = 0.1
    INTEGRAL_HS_PID = 0.1

    LANDING_ANGLE_DELTA_PER_SEC = 3
    TERMINAL_LANDING_ALTITUDE = 150
    MIN_FUEL_NEEDED_ON_TOUCHDOWN = 0.1

    ACCEPTABLE_MARGIN_HS = 1
    ACCEPTABLE_MARGIN_ALT = 0.8
    ACCEPTABLE_MARGIN_VS = 2
    VERTICAL_LANDING_MIN_ANG = MIN_ANG
    VERTICAL_LANDING_MAX_ANG = abs(VERTICAL_LANDING_MIN_ANG)

    def __init__(self, shared_state: SharedState):
        super().__init__(shared_state)
        self._current_landing_state = self.STATE_ASCENDING

        self.min_ang = self.MIN_ANG
        self.max_ang = self.MAX_ANG
        self.target_vs = self.TARGET_VS
        self.target_hs = None

        self.pid_vs = PID(1, self.INTEGRAL_VS_PID, 0.05, 5)
        self.pid_hs = PID(1, self.INTEGRAL_HS_PID, 0.05, 5)
        self.pid_ang = PID(0.5, 0.05, 0.01, 3)

        self.been_below_terminal_altitude = False

        self._first_apogee = None

    def has_landed_ok(self, current_state):
        return self._current_landing_state == self.STATE_DESCENDING and current_state.hs <= self.ACCEPTABLE_MARGIN_HS and \
               current_state.hs >= -self.ACCEPTABLE_MARGIN_HS and \
               current_state.alt < self.ACCEPTABLE_MARGIN_ALT and \
               current_state.alt > -self.ACCEPTABLE_MARGIN_ALT and \
               current_state.vs < self.ACCEPTABLE_MARGIN_VS and \
               current_state.vs > -self.ACCEPTABLE_MARGIN_VS

    def handler_ascending(self, current_state):
        self.target_hs = self.TARGET_HS if current_state.alt >= 100 else 0
        self.target_vs = -self.TARGET_VS

        if current_state.alt >= 1000:
            self._current_landing_state = self.STATE_APOGEE

    def handler_apogee(self, current_state):
        self.target_vs = 0
        self.target_hs = current_state.hs

        if not self._first_apogee:
            self._first_apogee = current_state.time

        if current_state.time - self._first_apogee >= 10:
            self._current_landing_state = self.STATE_DESCENDING

    def handler_descending(self, current_state):
        self.target_hs = 0
        self.target_vs = self.TARGET_VS

        self.target_vs = PID.constrain(current_state.alt * 1 / 10, 0.01, self.max_ang)

    def step(self, dt, current_state) -> SharedState:
        if self.has_landed_ok(current_state):
            if current_state.fuel >= self.MIN_FUEL_NEEDED_ON_TOUCHDOWN:
                raise SimulationEnded()

        if self._current_landing_state != self.STATE_ASCENDING and current_state.alt < -2:
            raise FtsActivatedException()

        if self._current_landing_state == self.STATE_ASCENDING:
            self.handler_ascending(current_state)
        elif self._current_landing_state == self.STATE_APOGEE:
            self.handler_apogee(current_state)
        elif self._current_landing_state == self.STATE_DESCENDING:
            self.handler_descending(current_state)

        error_hs = current_state.hs - self.target_hs
        error_vs = current_state.vs - self.target_vs

        out_pid_vs = self.pid_vs.update(error_vs, dt)
        out_pid_hs = self.pid_hs.update(error_hs, dt)

        diff_percent_pid_vs = PID.normalize(-self.TARGET_VS, self.TARGET_VS, out_pid_vs, 0, 2)
        diff_percent_pid_hs = PID.normalize(-self.TARGET_HS, self.TARGET_HS, out_pid_hs, 0, 2)

        final_ang_vs = (self.max_ang - self.min_ang) * (1 - diff_percent_pid_vs) + self.min_ang
        final_ang_hs = (self.max_ang - self.min_ang) * diff_percent_pid_hs + self.min_ang

        wanted_ang = (final_ang_hs + final_ang_vs) / 2
        error_wanted_ang = current_state.vehicle_ang - wanted_ang
        pid_error_ang = self.pid_ang.update(error_wanted_ang, dt)

        ret_state: SharedState = copy.deepcopy(current_state)
        ret_state.vehicle_ang = PID.constrain(current_state.vehicle_ang - pid_error_ang, self.min_ang, self.max_ang)
        ret_state.wanted_vehicle_ang = wanted_ang
        ret_state.wanted_hs = self.target_hs
        ret_state.wanted_vs = self.target_vs

        ret_state.thrust = (diff_percent_pid_hs + diff_percent_pid_vs) / 2
        ret_state.wanted_thrust = ret_state.thrust
        return ret_state

    @classmethod
    def get_initial_state(cls) -> SharedState:
        s = SharedState()
        s.vs = 0
        s.hs = 0
        s.distance = 0
        s.alt = 0
        s.fuel = 450

        return s
