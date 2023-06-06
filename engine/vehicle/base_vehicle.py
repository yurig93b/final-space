import abc

from data.sharedstate import SharedState


class BaseVehicle(object):

    def __init__(self, state: SharedState):
        self._state = state

    @classmethod
    @abc.abstractmethod
    def get_max_fuel(self):
        pass

    @abc.abstractmethod
    def get_engine_thrust_force(self):
        pass

    @abc.abstractmethod
    def get_engine_fuel_burn_rate_per_second(self):
        pass

    @abc.abstractmethod
    def get_weight(self, current_fuel):
        pass

    @abc.abstractmethod
    def get_per_second_fuel_burn(self):
        pass

    @abc.abstractmethod
    def get_pid_ang(self):
        pass

    @abc.abstractmethod
    def get_pid_thrust(self):
        pass