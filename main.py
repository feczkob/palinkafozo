from control import Control
from lcd import LCD
from program_state import ProgramState
from utime import sleep
from constants import display, HEATER_1, HEATER_2, HEATER_3

# Initial setup
HEATER_1.off()
HEATER_2.off()
HEATER_3.off()

# Program state
state = ProgramState()

# Screen state
lcd = LCD(display, state)

# Control
control = Control()

while True:
    try:
        control.measure_temperature(state)
        lcd.handle_buttons(state)
        control.control_heaters(state)
        control.control_mixer(state)
        lcd.update_display(state)
        sleep(0.1)
    except KeyboardInterrupt:
        break