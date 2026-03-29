from constants import DS_SENSOR, HEATER_1, HEATER_2, HEATER_3, MIXER_PIN, roms
from pid import PidController
from program_state import ProgramState

class Control:
    def __init__(self, pid: PidController):
        self.pid = pid
    
    def measure_temperature(self, state: ProgramState):
        DS_SENSOR.convert_temp()
        measured = DS_SENSOR.read_temp(roms[0])
        
        #print("Measured temperature:", measured)
        state.set_measured_temp(measured)
        
    def control_heaters(self, state: ProgramState):
        #print("Target temp:", state.get_target_temp_for_phase(), "Measured temp:", state.measured_temp)
        
        # Calculate PID output
        pid_output = self.pid.calculate_pid_output(state)
        
        # Determine which heaters should be active
        heaters_in_use = self.pid.determine_heater_states(pid_output)
        
        state.switch_heaters(heaters_in_use)
        
        # Apply heater states to hardware
        HEATER_1.value(state.calculate_heater_state(0))
        HEATER_2.value(state.calculate_heater_state(1))
        HEATER_3.value(state.calculate_heater_state(2))
            
    def control_mixer(self, state: ProgramState):
        if state.mix:
            MIXER_PIN.on()
        else:
            MIXER_PIN.off()