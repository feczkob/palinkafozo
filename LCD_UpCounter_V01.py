'''
 Demonstrates the use of 1602 LCD Keypad shield with RPi Pico.
 
 * 16x2 LCD Connection diagram
 * LCD 4 bit mode interface
 * Displaying welcome screen
 * Clear Display, Cursor on, Cursor Off, Backlight On, Back light Off
 * Write Command, Write data functionalities
  
 * The Raspberry Pi Pico pin connections for 16x2 LCD Keypad shield are given below:
 
 # LCD Power Pins
 * 16x2 LCD VCC pin to VBUS
 * 16x2 LCD GND pin to GND
 
 # LCD Data Pins
 * 16x2 LCD D4 pin to GPIO0
 * 16x2 LCD D5 pin to GPIO1
 * 16x2 LCD D6 pin to GPIO2
 * 16x2 LCD D7 pin to GPIO3
 
 # LCD Control Pins
 * 16x2 LCD RS pin to GPIO4
 * 16x2 LCD ENABLE pin to GPIO5
 * 16x2 LCD BACK LIGHT pin to GPIO6
 
 # Caution do not connect A0 pin of shield to RPi Pico.
 # Potential divided key connections, provides +5VDC output.
  
 Name:- M.Pugazhendi
 Date:-  13thJul2021
 Version:- V0.1
 e-mail:- muthuswamy.pugazhendi@gmail.com
'''

# Import time
import time

from constants import *

display.BackLightOn()

# Line one string
display.WriteLine('Raspberry Pi',1)

# Line two string
display.WriteLine('Pico 16x2 LCD',2)
time.sleep(5)

count = 250
while True:
    # Clear Screen
    display.ClearScreenCursorHome()
    
    #Count up
    count = count + 1
    
    #Write into LCD
    #display.WriteLine(f'   UP COUNTER ▲',1)
    display.WriteLine('       ' + str(count),2)
    
    #Wair for two seconds
    time.sleep(2)