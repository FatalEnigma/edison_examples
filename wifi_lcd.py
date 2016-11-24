import socket
import fcntl
import struct
import random
import time

from upm import pyupm_i2clcd as lcd
from upm import pyupm_grove as grove

def get_ip_address(ifname):

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915,  # SIOCGIFADDR
                                        struct.pack('256s', ifname[:15])
                                            )[20:24])

screen_colours = [(255,0,0), (0,255,0), (0,0,255), (255,128,0), (255,255,0), (0,255,255), (255,0,255), (127,0,255)]

# Initialize Jhd1313m1 at 0x3E (LCD_ADDRESS) and 0x62 (RGB_ADDRESS)
myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

# Clear
myLcd.clear()

# Green
myLcd.setColor(*random.choice(screen_colours))

# Zero the cursor
myLcd.setCursor(0,0)

# Print it.
ip_address = get_ip_address('wlan0')
myLcd.write(ip_address)

# Set up the button
button = grove.GroveButton(4)

pressed = False
while 1:
    if (button.value() == 1) and pressed == False:
        myLcd.setColor(*random.choice(screen_colours))
        print ("button pressed")
        pressed = True
    elif (button.value() == 0) and (pressed == True):
        pressed = False

del myLcd
del button
    

