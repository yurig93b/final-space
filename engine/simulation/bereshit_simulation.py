import math

from data.sharedstate import SharedState
from pid.pid import PID
from simulation.base_simulation import BaseSimulation
from simulation.fts_activated import FtsActivatedException
from simulation.simulation_ended import SimulationEnded
import copy


class BereshitSimulation(BaseSimulation):
    STATE_ENTERING = 0
    STATE_CHAGING_TO_VERTICAL_POSITION = 1
    STATE_VERTICAL_LANDING = 2

    TARGET_VS = 25
    MIN_ANG = 58.02236798
    MAX_ANG = 77.47671845
    FINAL_ALT = 2000.0
    LANDING_TARGET_VS = 20.0

    INTEGRAL_VS_PID = 0.2
    INTEGRAL_HS_PID = 0.05

    LANDING_ANGLE_DELTA_PER_SEC = 3
    TERMINAL_LANDING_ALTITUDE = 150
    MIN_FUEL_NEEDED_ON_TOUCHDOWN = 0.1

    ACCEPTABLE_MARGIN_HS = 1
    ACCEPTABLE_MARGIN_ALT = 0.8
    ACCEPTABLE_MARGIN_VS = 2
    VERTICAL_LANDING_MIN_ANG = -4
    VERTICAL_LANDING_MAX_ANG = abs(VERTICAL_LANDING_MIN_ANG)

    def __init__(self, shared_state: SharedState):
        super().__init__(shared_state)
        self._current_landing_state = self.STATE_ENTERING

        self.min_ang = self.MIN_ANG
        self.max_ang = self.MAX_ANG
        self.target_vs = self.TARGET_VS
        self.target_hs = None

        self.pid_vs = PID(2.5, self.INTEGRAL_VS_PID, 0.05, 300)
        self.pid_hs = PID(2.5, self.INTEGRAL_HS_PID, 0.05, 300)
        self.pid_ang = PID(0.9, 0.1, 0.01, 10)

        self.been_below_terminal_altitude = False



    def has_landed_ok(self, current_state):
        return current_state.hs <= self.ACCEPTABLE_MARGIN_HS and \
                current_state.hs >= -self.ACCEPTABLE_MARGIN_HS and \
                current_state.alt < self.ACCEPTABLE_MARGIN_ALT and \
                current_state.alt > -self.ACCEPTABLE_MARGIN_ALT and \
                current_state.vs < self.ACCEPTABLE_MARGIN_VS and \
                current_state.vs > -self.ACCEPTABLE_MARGIN_VS
    
    def update_pid_controllers_if_no_hs(self):
        self._current_landing_state = self.STATE_CHAGING_TO_VERTICAL_POSITION
        self.min_ang = self.VERTICAL_LANDING_MIN_ANG
        self.max_ang = self.VERTICAL_LANDING_MAX_ANG
        self.pid_vs = PID(0.7, 0.05, 0.05, 5)
        self.pid_vs = PID(0.7, 0.05, 0.05, 5)

    def step(self, dt, current_state) -> SharedState:
        if self.has_landed_ok(current_state):
            if current_state.fuel >= self.MIN_FUEL_NEEDED_ON_TOUCHDOWN:
                raise SimulationEnded()

        if current_state.alt < -2:
            raise FtsActivatedException()
        
        if current_state.hs <= 0 and self._current_landing_state == self.STATE_ENTERING:
            self.update_pid_controllers_if_no_hs()

        if self._current_landing_state == self.STATE_VERTICAL_LANDING:
            if self.been_below_terminal_altitude or current_state.alt < self.TERMINAL_LANDING_ALTITUDE:
                self.been_below_terminal_altitude = True
                self.target_vs = PID.constrain(current_state.alt * 1 / 10, 0.5, 5)
            else:
                self.target_vs = self.LANDING_TARGET_VS

        lose_hs_per_sec = current_state.vs / 10

        if self._current_landing_state >= self.STATE_CHAGING_TO_VERTICAL_POSITION:
            self.target_hs = 0
        else:
            self.target_hs = current_state.hs - lose_hs_per_sec * dt

        error_hs = current_state.hs - self.target_hs
        error_vs = current_state.vs - self.target_vs

        out_pid_vs = self.pid_vs.update(error_vs, dt)
        out_pid_hs = self.pid_hs.update(error_hs, dt)

        diff_percent_pid_vs = PID.normalize(-5, 20, out_pid_vs, 0, 2)
        diff_percent_pid_hs = PID.normalize(-200, 400, out_pid_hs, 0, 1)

        diff_percent_pid_hs_state_landing = PID.normalize(self.VERTICAL_LANDING_MIN_ANG, self.VERTICAL_LANDING_MAX_ANG,
                                                          out_pid_hs, -1, 1)

        final_ang_vs = (self.max_ang - self.min_ang) * (1 - diff_percent_pid_vs) + self.min_ang

        if self._current_landing_state == self.STATE_ENTERING:
            final_ang_hs = (self.max_ang - self.min_ang) * diff_percent_pid_hs + self.min_ang
        else:
            final_ang_hs = (self.max_ang - self.min_ang) * diff_percent_pid_hs_state_landing + self.min_ang

        if self._current_landing_state == self.STATE_CHAGING_TO_VERTICAL_POSITION:
            wanted_ang = PID.constrain(self.min_ang - self.LANDING_ANGLE_DELTA_PER_SEC * dt, 0, self.max_ang)
        elif self._current_landing_state == self.STATE_VERTICAL_LANDING:
            wanted_ang = final_ang_hs
        else:
            wanted_ang = (final_ang_hs + final_ang_vs) / 2

        if self._current_landing_state == self.STATE_CHAGING_TO_VERTICAL_POSITION:
            if abs(self.min_ang) <= self.VERTICAL_LANDING_MAX_ANG:
                self._current_landing_state = self.STATE_VERTICAL_LANDING
                self.pid_hs.reset()
                self.pid_vs.reset()

        error_wanted_ang = current_state.vehicle_ang - wanted_ang
        pid_error_ang = self.pid_ang.update(error_wanted_ang, dt)

        ret_state :SharedState = copy.deepcopy(current_state)
        ret_state.vehicle_ang = PID.constrain(current_state.vehicle_ang - pid_error_ang, self.min_ang, self.max_ang)
        ret_state.wanted_vehicle_ang = wanted_ang
        ret_state.wanted_hs = self.target_hs
        ret_state.wanted_vs = self.target_vs

        if self._current_landing_state == self.STATE_CHAGING_TO_VERTICAL_POSITION:
            ret_state.thrust = 0
        elif self._current_landing_state == self.STATE_VERTICAL_LANDING:
            ret_state.thrust = diff_percent_pid_vs
        else:
            ret_state.thrust = (diff_percent_pid_hs + diff_percent_pid_vs) / 2

        return ret_state

    @classmethod
    def get_initial_state(cls) -> SharedState:
        s = SharedState()
        s.dt = 0
        s.vs = 24.8
        s.hs = 932.0
        s.distance = 181 * 1000.0
        s.alt = 13748.0
        s.fuel = 121.0
        s.thrust = 0

        return s

