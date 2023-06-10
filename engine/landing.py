import math

import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize

from moon import Moon
from pid import PID


class Landing(object):
    WEIGHT_EMP = 165.0
    WEIGHT_FULE = 420.0
    WEIGHT_FULL = WEIGHT_EMP + WEIGHT_FULE
    MAIN_ENG_F = 430.0
    SECOND_ENG_F = 25.0
    MAIN_BURN = 0.15
    SECOND_BURN = 0.009
    ALL_BURN = MAIN_BURN + 8 * SECOND_BURN

    def __init__(self, vs=24.8, hs=932.0, alt=13748.0, ang=58.3, fuel=121.0, min_fuel=15.0, need_plot=True,
                 need_csv=True):
        self.fuel = None
        self.ang = None
        self.alt = None
        self.hs = None
        self.vs = None

        self._vs = vs
        self._hs = hs
        self._alt = alt
        self._ang = ang
        self._fuel = fuel

        self.need_plot = need_plot
        self.need_csv = need_csv
        self.min_fuel = min_fuel

        self.reset()

    def reset(self):
        self.vs = self._vs
        self.hs = self._hs
        self.alt = self._alt
        self.ang = self._ang
        self.fuel = self._fuel

    @classmethod
    def accMax(cls, weight):
        return cls.acc(weight, True, 8)

    @classmethod
    def acc(cls, weight, main, seconds):
        t = 0
        if main:
            t += cls.MAIN_ENG_F
        t += seconds * cls.SECOND_ENG_F
        ans = t / weight
        return ans

    def land(self, a):  # TARGET_VS = 23.0, MAX_ANG = 70.0, MIN_ANG = 50.0):
        TARGET_VS = a[0]
        MIN_ANG = a[1]
        MAX_ANG = a[2]
        FINAL_ALT = a[3]
        LANDING_TARGET_VS = a[4]

        INTEGRAL_VS = 0.2
        INTEGRAL_HS = 0.05
        LANDING_ANGLE_DELTA_PER_SEC = 3
        TERMINAL_LANDING_ALTITUDE = 150
        MIN_FUEL_NEEDED_ON_TOUCHDOWN = 1

        ACCEPTABLE_MARGIN_HS = 1
        ACCEPTABLE_MARGIN_ALT = 0.8
        ACCEPTABLE_MARGIN_VS = 2
        VERTICAL_LANDING_MIN_ANG = -4
        VERTICAL_LANDING_MAX_ANG = abs(VERTICAL_LANDING_MIN_ANG)

        NN = 0.7

        dist = 181 * 1000.0
        time = 0.0
        dt = 1
        acc = 0.0
        weight = self.WEIGHT_EMP + self.fuel

        TARGET_HS_FINAL_ALT = 100.0

        VS_PID = PID(2.5, INTEGRAL_VS, 0.05, 300)
        HS_PID = PID(2.5, INTEGRAL_HS, 0.05, 300)
        ANG_PID = PID(0.9, 0.1, 0.01, 10)

        data_vs = []
        data_hs = []
        data_alt = []
        data_ang = []
        data_fuel = []

        STATE_ENTERING = 0
        STATE_CHAGING_TO_VERTICAL_POSITION = 1
        STATE_VERTICAL_LANDING = 2

        current_state = STATE_ENTERING

        self.reset()

        while True:
            #
            # if hs <= 0:
            #     con = alt>=0 and hs >= -0.5  and alt>350 and fuel > 28 and alt < 1000
            #     if con:
            #         print((fuel, alt, vs, hs, a))
            #         return -alt
            #     return np.inf

            if self.need_csv and time % 1 == 0:
                if time % 4:
                    print("alt,time,vs,target_vs, hs,dist,ang,weight,acc,fuel")
                print("{},{},{},{},{},{},{},{},{},{}".format(self.alt, time, self.vs, TARGET_VS, self.hs, dist,
                                                                   self.ang, weight, acc,
                                                                   self.fuel))

            # Append data for collectioj
            data_vs.append(self.vs)
            data_hs.append(self.hs)
            data_alt.append(self.alt)
            data_ang.append(self.ang)
            data_fuel.append(self.fuel)


            landed_ok = self.hs <= ACCEPTABLE_MARGIN_HS and \
                        self.hs >= -ACCEPTABLE_MARGIN_HS and \
                        self.alt < ACCEPTABLE_MARGIN_ALT and \
                        self.alt > -ACCEPTABLE_MARGIN_ALT and \
                        self.vs < ACCEPTABLE_MARGIN_VS and \
                        self.vs > -ACCEPTABLE_MARGIN_VS

            if landed_ok:
                if self.need_plot and self.fuel >= MIN_FUEL_NEEDED_ON_TOUCHDOWN:
                    fig = plt.figure(1)
                    fig.suptitle("ALT")
                    plt.plot(data_alt, label='alt')
                    fig = plt.figure(2)
                    fig.suptitle("VS")

                    plt.plot(data_vs, label='vs')
                    fig = plt.figure(3)
                    fig.suptitle("HS")

                    plt.plot(data_hs, label='hs')
                    fig = plt.figure(4)
                    fig.suptitle("ANG")

                    plt.plot(data_ang, label='ang')

                    fig = plt.figure(5)
                    fig.suptitle("FUEL")
                    plt.plot(data_fuel, label='ang')

                    plt.show()
                if self.fuel >= MIN_FUEL_NEEDED_ON_TOUCHDOWN:
                    print("fuel_left, alt, vs, hs, flight_config")
                    print((self.fuel, self.alt, self.vs, self.hs, a))
                return -(self.fuel)

            if self.alt < -2:
                return np.inf

            if self.hs <= 0 and current_state == STATE_ENTERING:
                current_state = STATE_CHAGING_TO_VERTICAL_POSITION
                MIN_ANG = VERTICAL_LANDING_MIN_ANG
                MAX_ANG = VERTICAL_LANDING_MAX_ANG
                VS_PID = PID(0.7, 0.05, 0.05, 5)
                HS_PID = PID(0.7, 0.05, 0.05, 5)

            been_below_terminal_altitude = False
            if current_state == STATE_VERTICAL_LANDING:
                if been_below_terminal_altitude or self.alt < TERMINAL_LANDING_ALTITUDE:
                    been_below_terminal_altitude = True
                    TARGET_VS = PID.constrain(self.alt * 1 / 10, 0.5, 5)
                else:
                    TARGET_VS = LANDING_TARGET_VS


            LOSE_HS_PER_SEC = self.vs / 10
            if current_state >= STATE_CHAGING_TO_VERTICAL_POSITION:
                target_hs = 0
            else:
                target_hs = self.hs - LOSE_HS_PER_SEC * dt  # self.alt * ALT_FACTOR * TARGET_HS_FINAL_ALT / FINAL_ALT
            error_hs = self.hs - target_hs
            error_vs = self.vs - TARGET_VS
            out_pid_vs = VS_PID.update(error_vs, dt)
            out_pid_hs = HS_PID.update(error_hs, dt)

            diff_percent_pid_vs = PID.normalize(-5, 20, out_pid_vs, 0, 2)
            diff_percent_pid_hs = PID.normalize(-200, 400, out_pid_hs, 0, 1)

            diff_percent_pid_hs_state_landing = PID.normalize(VERTICAL_LANDING_MIN_ANG, VERTICAL_LANDING_MAX_ANG,
                                                              out_pid_hs, -1, 1)

            final_ang_vs = (MAX_ANG - MIN_ANG) * (1 - diff_percent_pid_vs) + MIN_ANG

            if current_state == STATE_ENTERING:
                final_ang_hs = (MAX_ANG - MIN_ANG) * diff_percent_pid_hs + MIN_ANG
            else:
                final_ang_hs = (MAX_ANG - MIN_ANG) * diff_percent_pid_hs_state_landing + MIN_ANG

            if current_state == STATE_CHAGING_TO_VERTICAL_POSITION:
                wanted_ang = PID.constrain(self.ang - LANDING_ANGLE_DELTA_PER_SEC * dt, 0, MAX_ANG)
            elif current_state == STATE_VERTICAL_LANDING:
                wanted_ang = final_ang_hs
            else:
                wanted_ang = (final_ang_hs + final_ang_vs) / 2

            if current_state == STATE_CHAGING_TO_VERTICAL_POSITION:
                if abs(self.ang) <= 3:
                    current_state = STATE_VERTICAL_LANDING
                    HS_PID.reset()
                    VS_PID.reset()

            error_wanted_ang = self.ang - wanted_ang
            pid_error_ang = ANG_PID.update(error_wanted_ang, dt)
            self.ang = PID.constrain(self.ang - pid_error_ang, MIN_ANG, MAX_ANG)

            if current_state == STATE_CHAGING_TO_VERTICAL_POSITION:
                NN = 0
            elif current_state == STATE_VERTICAL_LANDING:
                NN = diff_percent_pid_vs
            else:
                NN = (diff_percent_pid_hs + diff_percent_pid_vs) / 2

            ang_rad = math.radians(self.ang)
            h_acc = math.sin(ang_rad) * acc
            v_acc = math.cos(ang_rad) * acc
            vacc = Moon.getAcc(self.hs)
            time += dt

            dw = dt * self.ALL_BURN * NN
            if self.fuel > 0:
                self.fuel -= dw
                weight = self.WEIGHT_EMP + self.fuel
                acc = NN * self.accMax(weight)
            else:
                acc = 0
                return np.inf

            v_acc -= vacc
            self.hs -= h_acc * dt
            dist -= self.hs * dt
            self.vs -= v_acc * dt
            self.alt -= dt * self.vs


passing_configs = []
best_config = None
best_fuel = np.inf

original_params = {"vs": 24.8,
                   "hs": 932.0,
                   "alt": 13748.0,
                   "ang": 58.3,
                   "fuel": 121.0,
                   "need_csv": False,
                   "need_plot": True}


def check_iter(flight_configuration, verbose=True, should_exit = True):
    # Check +- 10% of error in starting point. Note that the margin is applied to one variable at a time.
    # as we consider a change in more than 1 variable a change that is not within margin of error.
    import copy
    for possible_error in [1.0, 1.1, 0.9]:
        for possible_variable in ["vs", "alt", "ang", "fuel"]:
            altered_params = copy.deepcopy(original_params)
            altered_params[possible_variable] = possible_error * altered_params[possible_variable]
            print("\n")
            print("Running with params with error {} on {}".format(possible_error, possible_variable))
            print(altered_params)
            res = Landing(**altered_params).land(flight_configuration)
            if res == np.inf:
                print("FAILED on {}".format(possible_variable))
                print("\n")
                return

    passing_configs.append(flight_configuration)
    if verbose:
        print(flight_configuration)
    if should_exit:
        exit(0)

def optimize_landing():
    from scipy.optimize import Bounds
    bounds = Bounds([20, 45, 60, 2000, 15], [30, 60, 80, 4000, 30])
    l = Landing(need_csv=False, need_plot=False, min_fuel=1)
    results = dict()
    results['shgo'] = optimize.shgo(l.land, bounds, iters=4, callback=check_iter)
    print(results['shgo'])


if __name__ == "__main__":
    # Target VS, Min Ang, Max Ang, Target altitude for 100 hs, Target Landing speed when vertical
    # The flight config was obtained by optimize_landing function
    flight_configuration = [25, 58.02236798, 77.47671845, 2000., 20]
    check_iter(flight_configuration)

