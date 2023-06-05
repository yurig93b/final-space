class PID(object):
    def __init__(self, p, i, d, max_i):
        self.p = p
        self.i = i
        self.d = d
        self.max_i = max_i
        self.last_error = 0
        self.first_run = True
        self.current_integral = 0

    def update(self, error, dt):
        if self.first_run:
            self.last_error = error
            self.first_run = False

        diff = (error - self.last_error) / dt
        self.last_error = error
        self.current_integral = self.constrain(self.current_integral + self.i * error, -self.max_i, self.max_i)
        return self.p * error + self.current_integral + diff * self.d

    def reset(self):
        self.current_integral = 0
        self.first_run = True

    @classmethod
    def constrain(cls, val, min_val, max_val):
        return max(min(val, max_val), min_val)

    @classmethod
    def normalize(cls, old_min, old_max, old_val, new_min, new_max):
        return cls.constrain((old_val - old_min) * (new_max - new_min) / (old_max - old_min) + new_min, new_min,
                             new_max)
