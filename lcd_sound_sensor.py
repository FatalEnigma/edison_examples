import socket
import fcntl
import struct
import random
import time
import math

from upm import pyupm_i2clcd as lcd
from upm import pyupm_grove as grove
from upm import pyupm_mic as mic

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

# Setup Mic
myMic = mic.Microphone(1)
threshContext = mic.thresholdContext()
threshContext.averageReading = 0
threshContext.runningAverage = 0
threshContext.averagedOver = 1
max_thresh = 0

while 1:
    myLcd.setColor(*random.choice(screen_colours))
    buffer = mic.uint16Array(128)
    len = myMic.getSampledWindow(2, 128, buffer)
    
    if len:
        thresh = myMic.findThreshold(threshContext,30, buffer, len)
        myLcd.clear()
        myLcd.setCursor(0,0)
        x = int(math.floor(thresh / 10))
        myLcd.write("*" * x)


del myLcd
