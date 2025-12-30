
from utime import sleep
from constants import BUTTONS_PIN_ADC, CHAR_HEATER, CHAR_HEATER_ENABLED_OFF, CHAR_HEATER_ENABLED_ON, CHAR_MIX, CHAR_MIX_OFF, CHAR_MIX_ON, CHAR_TARGET, CHAR_THERMOMETER
from program_state import ProgramState


class LCD:
    def __init__(self, display, state: ProgramState):
        self.display = display
        self.backlight_on()

        # Create custom characters
        self.display.CreateChar(slot=0, bitmap=CHAR_HEATER_ENABLED_OFF)
        self.display.CreateChar(slot=1, bitmap=CHAR_TARGET)
        self.display.CreateChar(slot=2, bitmap=CHAR_THERMOMETER)
        self.display.CreateChar(slot=3, bitmap=CHAR_HEATER_ENABLED_ON)
        self.display.CreateChar(slot=4, bitmap=CHAR_HEATER)
        self.display.CreateChar(slot=5, bitmap=CHAR_MIX)
        self.display.CreateChar(slot=6, bitmap=CHAR_MIX_ON)
        self.display.CreateChar(slot=7, bitmap=CHAR_MIX_OFF)
        
        self.target_temp: float = state.get_target_temp_for_phase()
        self.measured_temp: float = state.measured_temp
        self.phase = state.phase
        self.mix = state.mix
        self.heaters_enabled = state.heaters_enabled.copy()
        self.heaters_in_use = state.heaters_in_use.copy()

    def backlight_on(self):
        self.display.BackLightOn()

    def backlight_off(self):
        self.display.BackLightOff()
        
    def handle_buttons(self, state: ProgramState):
        buttons_adc = BUTTONS_PIN_ADC.read_u16()
        #print("Buttons ADC value:", buttons_adc)
    
        if 200 <= buttons_adc < 5000:
            # RIGHT
            if(sum(state.heaters_enabled) == 0): 
                state.heaters_enabled = [True, True, True]
                sleep(0.3)  # Simple debounce
                return
            state.heaters_enabled[sum(state.heaters_enabled) - 1] = False
            sleep(0.3)  # Simple debounce
        elif 5000 <= buttons_adc < 11000:
            # UP
            state.change_target_temp_for_phase_by(0.1)
            #print("Increased target temperature to:", round(TARGET_TEMPERATURE[phase - 1], 1))
        elif 11000 <= buttons_adc < 17000:
            # DOWN
            state.change_target_temp_for_phase_by(-0.1)
            #print("Decreased target temperature to:", round(TARGET_TEMPERATURE[phase - 1], 1))
        elif 17000 <= buttons_adc < 26000:
            # LEFT
            state.switch_mix()
            sleep(0.3)  # Simple debounce
        elif 26000 <= buttons_adc < 38000:
            # SELECT
            state.switch_phase()
            sleep(0.3)  # Simple debounce
    
    def update_display(self, state: ProgramState):
        if (round(self.target_temp, 1) == round(state.get_target_temp_for_phase(), 1) and
            round(self.measured_temp, 1) == round(state.measured_temp, 1) and
            self.phase == state.phase and
            self.mix == state.mix and
            self.heaters_enabled == state.heaters_enabled and
            self.heaters_in_use == state.heaters_in_use):
            return  # No changes, skip updating the display
        
        self.target_temp = state.get_target_temp_for_phase()
        self.measured_temp = state.measured_temp
        self.phase = state.phase
        self.mix = state.mix
        self.heaters_in_use = state.heaters_in_use.copy()
        self.heaters_enabled = state.heaters_enabled.copy()
        
        self.display.ClearScreenCursorHome()
        
        # First row
        # Temperatures
        self.display.WriteLine(f"  {round(self.target_temp, 1)}C    {round(self.measured_temp, 1)}C", 1)
        # Target temperature
        self.display.DrawCustomChar(line_number=1, col=1, slot=1)
        # Measured temperature
        self.display.DrawCustomChar(line_number=1, col=10, slot=2)
        
        # Second row
        # Phase
        self.display.WriteLine(f"F{self.phase}", 2)
        # Mixer icon
        self.display.DrawCustomChar(line_number=2, col=8, slot=5)
        # Mixer on/off
        if(self.mix):
            self.display.DrawCustomChar(line_number=2, col=9, slot=6)
        else:
            self.display.DrawCustomChar(line_number=2, col=9, slot=7)
        # Heater icon
        self.display.DrawCustomChar(line_number=2, col=13, slot=4)
        # Heaters on/off
        if(self.heaters_enabled[0]): 
            if (self.heaters_in_use[0]): self.display.DrawCustomChar(line_number=2, col=14, slot=3)
            else: self.display.DrawCustomChar(line_number=2, col=14, slot=0)
        if(self.heaters_enabled[1]): 
            if (self.heaters_in_use[1]): self.display.DrawCustomChar(line_number=2, col=15, slot=3)
            else: self.display.DrawCustomChar(line_number=2, col=15, slot=0)
        if(self.heaters_enabled[2]): 
            if (self.heaters_in_use[2]): self.display.DrawCustomChar(line_number=2, col=16, slot=3)
            else: self.display.DrawCustomChar(line_number=2, col=16, slot=0)