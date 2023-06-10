import abc

from data.sharedstate import SharedState


class BaseSimulation(abc.ABC):
    def __init__(self, shared_state: SharedState):
        self.shared_state = shared_state

    @abc.abstractmethod
    def step(self, dt, current_state) -> SharedState:
        pass

    @classmethod
    @abc.abstractmethod
    def get_initial_state(self) -> SharedState:
        pass