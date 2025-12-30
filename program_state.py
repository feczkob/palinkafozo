from constants import TARGET_TEMPERATURE

class ProgramState:
    def __init__(self):
        self.target_temp: list[float] = TARGET_TEMPERATURE
        self.measured_temp: float = 0.0
        self.phase = 1
        self.mix = False
        self.heaters_in_use = [False, False, False]
        self.heaters_enabled = [True, True, True]
        
    def get_target_temp_for_phase(self) -> float:
        if 1 <= self.phase <= len(self.target_temp):
            return self.target_temp[self.phase - 1]
        else:
            raise ValueError("Phase out of range")
        
    def change_target_temp_for_phase_by(self, temperature: float):
        if 1 <= self.phase <= len(self.target_temp):
            self.target_temp[self.phase - 1] += temperature
        else:
            raise ValueError("Phase out of range")
        
    def switch_mix(self):
        self.mix = not self.mix
        
    def switch_phase(self):
        self.phase = (self.phase % 4) + 1
        
    def set_measured_temp(self, temperature: float):
        self.measured_temp = temperature
        
    def switch_heaters(self, states: list[bool]):
        self.heaters_in_use = states
        
    def calculate_heater_state(self, index: int) -> bool:
        if 0 <= index < len(self.heaters_in_use):
            return self.heaters_in_use[index] and self.heaters_enabled[index]
        else:
            raise IndexError("Heater index out of range")
        
    def should_activate_heaters(self) -> bool:
        return self.measured_temp < self.get_target_temp_for_phase()