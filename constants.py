import machine
import lcd_4bit_mode
import onewire
import ds18x20

RS = machine.Pin(4,machine.Pin.OUT)
ENABLE = machine.Pin(5,machine.Pin.OUT)
BACK_LIGHT = machine.Pin(6,machine.Pin.OUT)
D4 = machine.Pin(0,machine.Pin.OUT)
D5 = machine.Pin(1,machine.Pin.OUT)
D6 = machine.Pin(2,machine.Pin.OUT)
D7 = machine.Pin(3,machine.Pin.OUT)
HEATER_1 = machine.Pin(7,machine.Pin.OUT)
HEATER_2 = machine.Pin(8,machine.Pin.OUT)
HEATER_3 = machine.Pin(9,machine.Pin.OUT)
TEMPERATURE_PIN = machine.Pin(10, machine.Pin.IN)
DS_SENSOR = ds18x20.DS18X20(onewire.OneWire(TEMPERATURE_PIN))
MIXER_PIN = machine.Pin(11, machine.Pin.OUT)
BUTTONS_PIN = machine.Pin(27, machine.Pin.IN)
BUTTONS_PIN_ADC = machine.ADC(BUTTONS_PIN)

# TODO: actual values
TARGET_PHASE_1 = 23.0
TARGET_PHASE_2 = 26.0
TARGET_PHASE_3 = 28.0
TARGET_PHASE_4 = 30.0
TARGET_TEMPERATURE = [TARGET_PHASE_1, TARGET_PHASE_2, TARGET_PHASE_3, TARGET_PHASE_4]

display = lcd_4bit_mode.LCD16x2(RS,ENABLE,BACK_LIGHT,D4,D5,D6,D7)


# Custom LCD characters (5x8 bitmaps)
# Each byte represents one row, using only the lower 5 bits
RECTANGLE = [
    0b11111,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b11111
]

# Target temperature icon (crosshair/target)
CHAR_TARGET = [
    0b00100,
    0b01110,
    0b10101,
    0b11011,
    0b10101,
    0b01110,
    0b00100,
    0b00000
]

# Measured/actual temperature icon (thermometer)
CHAR_THERMOMETER = [
    0b00100,
    0b01010,
    0b01010,
    0b01010,
    0b01010,
    0b10001,
    0b10001,
    0b01110
]

# Heater ON icon (filled box with flame)
CHAR_HEATER = [
    0b00000,
    0b11111,
    0b10101,
    0b11011,
    0b10101,
    0b11011,
    0b10101,
    0b11111,
]

CHAR_HEATER_ON = [
    0b00000,
    0b01010,
    0b11111,
    0b10101,
    0b00000,
    0b01010,
    0b11111,
    0b10101,
]

# Mix ON icon (rotating arrows)
CHAR_MIX_ON = [
    0b00100,
    0b01110,
    0b11111,
    0b11111,
    0b11111,
    0b11111,
    0b01110,
    0b00100
]

# Mix OFF icon (static)
CHAR_MIX_OFF = [
    0b00000,
    0b01110,
    0b10001,
    0b10001,
    0b10001,
    0b10001,
    0b01110,
    0b00000
]

CHAR_MIX = [
    0b01111,
    0b00111,
    0b01101,
    0b11000,
    0b00011,
    0b10110,
    0b11100,
    0b11110,
]

# Phase
CHAR_PHASE = [
    0b00100,
    0b01010,
    0b01010,
    0b10001,
    0b10001,
    0b01010,
    0b01010,
    0b00100,
]