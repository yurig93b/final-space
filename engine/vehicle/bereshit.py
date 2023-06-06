from vehicle.base_vehicle import BaseVehicle


class BereshitVehicle(BaseVehicle):
    WEIGHT_VEHICLE = 165.0
    WEIGHT_FUEL = 420.0
    WEIGHT_FULL = WEIGHT_VEHICLE + WEIGHT_FUEL
    MAIN_ENG_F = 430.0
    SECOND_ENG_F = 25.0
    MAIN_BURN = 0.15
    SECOND_BURN = 0.009
    ALL_BURN = MAIN_BURN + 8 * SECOND_BURN

    @classmethod
    def get_max_fuel(cls):
        return cls.WEIGHT_FUEL

    def get_weight(self, current_fuel):
        return self.WEIGHT_VEHICLE + current_fuel

    def get_engine_thrust_force(self):
        return self.MAIN_ENG_F + 8 * self.SECOND_ENG_F

    def get_engine_fuel_burn_rate_per_second(self):
        return self.ALL_BURN

    def get_per_second_fuel_burn(self):
        return self.ALL_BURN

    def get_pid_ang(self):
        pass

    def get_pid_thrust(self):
        pass

