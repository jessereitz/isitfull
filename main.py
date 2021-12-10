from machine import ADC, Pin
import time

WATER_LEVEL_LOW = 2
WATER_LEVEL_MEDIUM = 30000
WATER_LEVEL_HIGH = 1.2

LED_LOW = Pin(18, Pin.OUT)
LED_MED = Pin(17, Pin.OUT)
LED_HIGH = Pin(16, Pin.OUT)

LEDs = [LED_LOW, LED_MED, LED_HIGH]
WATER_SENSOR = ADC(Pin(26))


def reading_to_voltage(reading):
    MAX_ADC_READING = 65535
    ADC_CONVERSION_FACTOR = 3.3 / (MAX_ADC_READING)
    return reading * ADC_CONVERSION_FACTOR


def reset_leds(target_light_vals):
    for index, val in enumerate(target_light_vals):
        if val:
            LEDs[index].on()
        else:
            LEDs[index].off()


def startup():
    for led in LEDs:
            led.on()
            time.sleep(0.25)

    time.sleep(0.5)

    for led in LEDs:
        led.off()
        time.sleep(0.25)

    for i in range(3):
        for led in LEDs:
            led.on()
        time.sleep(0.25)
        for led in LEDs:
            led.off()
        time.sleep(0.3)

    time.sleep(0.5)


def loop():
    while True:
        water_level = reading_to_voltage(WATER_SENSOR.read_u16())
        print('Water level reading:', water_level)
        target_light_vals = [False, False, False]

        if water_level <= WATER_LEVEL_HIGH:
            print('high')
            target_light_vals[2] = True
        elif water_level >= WATER_LEVEL_LOW:
            print('low')
            target_light_vals[0] = True
        else:
            print('medium')
            target_light_vals[1] = True

        print('Target led vals:', target_light_vals)
        reset_leds(target_light_vals)

        time.sleep(0.25)

startup()
loop()
