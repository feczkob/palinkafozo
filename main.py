from machine import Pin
from utime import sleep
from constants import *
import time


# Program state
TARGET_TEMPERATURE = 25.0
measured_temp: float = 0.0
mode = 1
heaters = [False, False, False]
HEATER_1.off()
HEATER_2.off()
HEATER_3.off()

interrupt_flag = 0
buttons_adc = 1024
debounce_time = 0

roms = DS_SENSOR.scan()
print('Found DS devices: ', roms)

# Screen state
screen_target_temp = TARGET_TEMPERATURE
screen_measured_temp = measured_temp
screen_mode = 1
screen_heater_status = heaters.copy()

def measure_temperature():   
    # TODO set precision?
    global measured_temp
    DS_SENSOR.convert_temp()
    measured = DS_SENSOR.read_temp(roms[0])
    
    #print("Measured temperature:", measured)
    measured_temp = measured

def control_heaters():
    global heaters, measured_temp, TARGET_TEMPERATURE
    # TODO: later we can take the direction (heating or cooling) into account
    if measured_temp < TARGET_TEMPERATURE:
        heaters = [True, True, True]
        HEATER_1.on()
        HEATER_2.on()
        HEATER_3.on()
        # print("Heaters ON")
    else:
        heaters = [False, False, False]
        HEATER_1.off()
        HEATER_2.off()
        HEATER_3.off()
        # print("Heaters OFF")
        
def print_heater_status(target_temp, measured_temp, mode, heaters):
    # TODO: store the screen state locally and only update if something changes
    global screen_target_temp, screen_measured_temp, screen_mode, screen_heater_status
    
    if (screen_target_temp == target_temp and
        screen_measured_temp == measured_temp and
        screen_mode == mode and
        screen_heater_status == heaters):
        return  # No changes, skip updating the display
    
    screen_target_temp = target_temp
    screen_measured_temp = measured_temp
    screen_mode = mode
    screen_heater_status = heaters.copy()
    
    display.ClearScreenCursorHome()
    display.WriteLine(f"S:{round(screen_target_temp, 1)}C  T:{round(screen_measured_temp, 1)}C", 1)
    display.WriteLine(f"Mod:{screen_mode}    Futes:{sum(screen_heater_status)}", 2)

def buttons_callback(pin):
    global buttons_adc, debounce_time
    print("Button interrupt triggered")

    current_time = time.ticks_ms()
    
    # Debounce check- only proceeds if 500ms has passed since the last trigger
    if time.ticks_diff(current_time, debounce_time) > 500:
        buttons_adc = BUTTONS_PIN_ADC.read_u16()
        print("Value on BUTTON ADC:", buttons_adc)
        debounce_time = current_time  # Update last debounce time

def handle_buttons():
    global TARGET_TEMPERATURE, buttons_adc, mode
    buttons_adc = BUTTONS_PIN_ADC.read_u16()
    if 200 <= buttons_adc < 6000:
        # RIGHT
        pass
    elif 6000 <= buttons_adc < 15000:
        # UP
        TARGET_TEMPERATURE += .1
        print("Increased target temperature to:", TARGET_TEMPERATURE)
    elif 15000 <= buttons_adc < 20000:
        # DOWN
        TARGET_TEMPERATURE -= 0.1
        print("Decreased target temperature to:", TARGET_TEMPERATURE)
    elif 20000 <= buttons_adc < 32000:
        # LEFT
        mode = (mode + 1) % 4
        sleep(0.3)  # Simple debounce
    elif 32000 <= buttons_adc < 40000:
        # SELECT
        pass
    reset_buttons_adc()
    
def reset_buttons_adc():
    # Reset buttons_adc to avoid repeated actions
    global buttons_adc
    buttons_adc = 1024

# TODO rising or falling?
#BUTTONS_PIN.irq(trigger=Pin.IRQ_FALLING|Pin.IRQ_RISING, handler=buttons_callback)
display.BackLightOn()
while True:
    try:
        measure_temperature()
        control_heaters()
        handle_buttons()
        print_heater_status(TARGET_TEMPERATURE, measured_temp, mode, heaters)
        sleep(0.1)
    except KeyboardInterrupt:
        break