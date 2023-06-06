from celestial_bodies.base_body import BaseBody


class Moon(BaseBody):
    RADIUS = 3475*1000
    ACC = 1.622
    EQ_SPEED = 1700

    @classmethod
    def get_radius(cls):
        return cls.RADIUS

    @classmethod
    def get_gravity_acc(cls):
        return cls.ACC

    @classmethod
    def get_eq_speed(cls):
        return cls.EQ_SPEED