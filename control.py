
from constants import DS_SENSOR, HEATER_1, HEATER_2, HEATER_3, MIXER_PIN
from program_state import ProgramState

roms = DS_SENSOR.scan()

class Control:
    def __init__(self):
        pass
    
    def measure_temperature(self, state: ProgramState):
        DS_SENSOR.convert_temp()
        measured = DS_SENSOR.read_temp(roms[0])
        
        #print("Measured temperature:", measured)
        state.set_measured_temp(measured)
        
    def control_heaters(self, state: ProgramState):
        # TODO: PID controller
        #print("Target temp:", state.get_target_temp_for_phase(), "Measured temp:", state.measured_temp)
        
        if state.should_activate_heaters():
            state.switch_heaters_on() 
        else:
            state.switch_heaters_off()
            
        HEATER_1.value(state.calculate_heater_state(0))
        HEATER_2.value(state.calculate_heater_state(1))
        HEATER_3.value(state.calculate_heater_state(2))
            
    def control_mixer(self, state: ProgramState):
        if state.mix:
            MIXER_PIN.on()
        else:
            MIXER_PIN.off()