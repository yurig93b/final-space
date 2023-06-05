from pid.pid import PID


class SharedState(object):
    def __init__(self, hs: float = 0,
                 wanted_hs: float = 0,
                 vs: float = 0,
                 wanted_vs: float = 0,
                 acc:float = 0,
                 distance: float = 0,
                 dt: float = 0,
                 time:float = 0,
                 vehicle_ang: float = 0,
                 wanted_vehicle_ang: float =0,
                 height: float = 0,
                 ang_relative_to_body: float = 0,
                 thrust: float = 0,
                 wanted_thrust: float = 0,
                 fuel: float = 0,
                 weight: float = 0):
        self.hs: float = hs
        self.wanted_hs: float = wanted_hs
        self.vs: float = vs
        self.wanted_vs: float = wanted_vs
        self.acc: float = acc
        self.distance: float = distance
        self.dt: float = dt
        self.time : float = time
        self.vehicle_ang: float = vehicle_ang
        self.wanted_vehicle_ang : float = wanted_vehicle_ang
        self.alt: float = height
        self.ang_relative_to_body: float = ang_relative_to_body
        self.thrust: float = thrust
        self.wanted_thrust: float = wanted_thrust
        self.fuel: float = fuel
        self.weight : float = weight