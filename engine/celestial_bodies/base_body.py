import abc


class BaseBody(abc.ABC):

    @classmethod
    @abc.abstractmethod
    def get_radius(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def get_gravity_acc(cls):
        pass

    @classmethod
    @abc.abstractmethod
    def get_eq_speed(cls):
        pass

    @classmethod
    def get_acc(cls, hs: float):
        n = abs(hs) / cls.get_eq_speed()
        return (1.0 - n) * cls.get_gravity_acc()
