import time
from upm import pyupm_grove as grove
def main():
    # Create the light sensor object using AIO pin 0
    light_sensor = grove.GroveLight(0)
    green_led = grove.GroveLed(2)

    while 1:
        print(light_sensor.value())
        if (light_sensor.value() < 10):
            green_led.on()
        else:
            green_led.off()

    del light_sensor
    del green_led


if __name__ == '__main__':
    main()
