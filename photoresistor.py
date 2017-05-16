#!/usr/local/bin/python

import time

import RPi.GPIO as GPIO


def rc_time(input_pin):
    count = 0
    # Output on the pin for
    GPIO.setup(input_pin, GPIO.OUT)
    GPIO.output(input_pin, GPIO.LOW)
    time.sleep(0.1)

    # Change the pin back to input
    GPIO.setup(input_pin, GPIO.IN)

    # Count until the pin goes high
    while (GPIO.input(input_pin) == GPIO.LOW):
        count += 1
    return count


def main():
    GPIO.setmode(GPIO.BOARD)
    input_pin = 18

    # Catch when script is interrupted, cleanup correct
    try:
        # Main loop
        while True:
            if (rc_time(input_pin) < 1000):
                # print "Someone has entered the room!"
                print rc_time(input_pin)
                time.sleep(.1)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
