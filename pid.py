from constants import CYCLE_TIME_SECONDS
from program_state import ProgramState

class PidController:
    def __init__(self, Kp: float = 1.0, Ki: float = 0.1, Kd: float = 0.02):
        # PID coefficients (to be tuned)
        # https://www.ni.com/en/shop/labview/pid-theory-explained.html
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain
        
        self.pid_last_error = 0.0
        
        self.integral = 0.0

    def calculate_pid_output(self, state: ProgramState) -> float:
        """Calculate PID output based on target and measured temperatures"""
        # Calculate error
        error = state.get_target_temp_for_phase() - state.measured_temp
        
        # Calculate PID output
        proportional = self.Kp * error
        self.integral += self.Ki * error * CYCLE_TIME_SECONDS
        derivative = self.Kd * (error - self.pid_last_error) / CYCLE_TIME_SECONDS
        
        output = proportional + self.integral + derivative
        
        # Update PID state
        self.pid_last_error = error
        
        # Return PID output
        return output

    def determine_heater_states(self, pid_output: float) -> list[bool]:
        """Determine which heaters should be active based on PID output"""
        # Determine heater states based on PID output
        # Higher positive output means more heating needed
        
        #print("PID output:", pid_output)
        
        # Define thresholds for heater activation
        if pid_output > 2.0:
            # All heaters on for maximum heating
            return [True, True, True]
        elif pid_output > 1.0:
            # Two heaters on for medium heating
            return [True, True, False]
        elif pid_output > 0.5:
            # One heater on for gentle heating
            return [True, False, False]
        else:
            # No heaters on (cooling or maintaining)
            return [False, False, False]