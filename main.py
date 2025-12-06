from machine import Pin
from utime import sleep
from constants import *
import time


# Program state
measured_temp: float = 0.0
phase = 1
mix = True
heaters_in_use = [False, False, False]
heaters_allowed = [True, True, True]
HEATER_1.off()
HEATER_2.off()
HEATER_3.off()

# Sensors
buttons_adc = 0
roms = DS_SENSOR.scan()

# Screen state
screen_target_temp = 0.0
screen_measured_temp = measured_temp
screen_phase = phase
screen_mix = mix
screen_heater_status = heaters_in_use.copy()

# Initialize LCD
display.BackLightOn()
display.CreateChar(slot=0, bitmap=CHAR_MIX)
display.CreateChar(slot=1, bitmap=CHAR_TARGET)
display.CreateChar(slot=2, bitmap=CHAR_THERMOMETER)
display.CreateChar(slot=3, bitmap=CHAR_HEATER_ON)
display.CreateChar(slot=4, bitmap=CHAR_HEATER)
display.CreateChar(slot=5, bitmap=CHAR_PHASE)
display.CreateChar(slot=6, bitmap=CHAR_MIX_ON)
display.CreateChar(slot=7, bitmap=CHAR_MIX_OFF)

def measure_temperature():   
    # TODO set precision?
    global measured_temp
    DS_SENSOR.convert_temp()
    measured = DS_SENSOR.read_temp(roms[0])
    
    #print("Measured temperature:", measured)
    measured_temp = measured

def control_heaters():
    global heaters_in_use, measured_temp, TARGET_TEMPERATURE
    if measured_temp < TARGET_TEMPERATURE[phase - 1]:
        heaters_in_use = [True, True, True]
        HEATER_1.value(heaters_in_use[0] & heaters_allowed[0])
        HEATER_2.value(heaters_in_use[1] & heaters_allowed[1])
        HEATER_3.value(heaters_in_use[2] & heaters_allowed[2])
    else:
        heaters_in_use = [False, False, False]
        HEATER_1.off()
        HEATER_2.off()
        HEATER_3.off()
      
def control_mixer():
    global mix
    if mix:
        MIXER_PIN.on()
    else:
        MIXER_PIN.off() 
        
def draw_to_lcd(target_temp, measured_temp, phase, heaters):
    global screen_target_temp, screen_measured_temp, screen_phase, screen_mix, screen_heater_status
    
    if (screen_target_temp == target_temp and
        screen_measured_temp == measured_temp and
        screen_phase == phase and
        screen_mix == mix and
        screen_heater_status == heaters):
        return  # No changes, skip updating the display
    
    screen_target_temp = target_temp
    screen_measured_temp = measured_temp
    screen_phase = phase
    screen_mix = mix
    screen_heater_status = heaters.copy()
    
    display.ClearScreenCursorHome()
    display.WriteLine(f"  {round(screen_target_temp, 1)}C    {round(screen_measured_temp, 1)}C", 1)
    # Target temperature
    display.DrawCustomChar(line_number=1, col=1, slot=1)
    # Measured temperature
    display.DrawCustomChar(line_number=1, col=10, slot=2)
    
    display.WriteLine(f" {screen_phase}", 2)
    # Phase icon
    display.DrawCustomChar(line_number=2, col=0, slot=5)
    # Mixer icon
    display.DrawCustomChar(line_number=2, col=8, slot=0)
    # Mixer on/off
    if(screen_mix):
        display.DrawCustomChar(line_number=2, col=9, slot=6)
    else:
        display.DrawCustomChar(line_number=2, col=9, slot=7)
    # Heater icon
    display.DrawCustomChar(line_number=2, col=13, slot=4)
    # Heaters on/off
    if(heaters[0]): display.DrawCustomChar(line_number=2, col=14, slot=3)
    if(heaters[1]): display.DrawCustomChar(line_number=2, col=15, slot=3)
    if(heaters[2]): display.DrawCustomChar(line_number=2, col=16, slot=3)

def handle_buttons():
    global TARGET_TEMPERATURE, buttons_adc, phase, mix, heaters_allowed
    buttons_adc = BUTTONS_PIN_ADC.read_u16()
    if 200 <= buttons_adc < 6000:
        # RIGHT
        if(sum(heaters_allowed) == 3): 
            heaters_allowed = [False, False, False]
            sleep(0.3)  # Simple debounce
            return
        heaters_allowed[sum(heaters_allowed)] = True
        sleep(0.3)  # Simple debounce
    elif 6000 <= buttons_adc < 14000:
        # UP
        TARGET_TEMPERATURE[phase - 1] += .1
        print("Increased target temperature to:", round(TARGET_TEMPERATURE[phase - 1], 1))
    elif 14000 <= buttons_adc < 20000:
        # DOWN
        TARGET_TEMPERATURE[phase - 1] -= .1
        print("Decreased target temperature to:", round(TARGET_TEMPERATURE[phase - 1], 1))
    elif 20000 <= buttons_adc < 32000:
        # LEFT
        mix = not mix
        sleep(0.3)  # Simple debounce
    elif 32000 <= buttons_adc < 40000:
        # SELECT
        phase = (phase % 4) + 1
        sleep(0.3)  # Simple debounce

def array_and(b1, b2):
    return [a and b for a, b in zip(b1, b2)]

while True:
    try:
        measure_temperature()
        handle_buttons()
        control_heaters()
        control_mixer()
        draw_to_lcd(
            TARGET_TEMPERATURE[phase - 1], 
            measured_temp, 
            phase, 
            array_and(heaters_in_use, heaters_allowed)
        )
        sleep(0.1)
    except KeyboardInterrupt:
        break