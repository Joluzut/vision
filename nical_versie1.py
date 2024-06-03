# This work is licensed under the MIT license.
# Copyright (c) 2013-2023 OpenMV LLC. All rights reserved.
# https://github.com/openmv/openmv/blob/master/LICENSE
#
# Hello World Example
#
# Welcome to the OpenMV IDE! Click on the green run arrow button below to run the script!

from machine import Pin
import time

toZumo = Pin("PA9", Pin.OUT_PP)

def check_zero_one(input_string):
    toZumo.low()
    for char in input_string:
        time.sleep_ms(1)
        if char == '0':
            toZumo.high()
        else:
            toZumo.low()

    time.sleep_ms(1)
    toZumo.high()
    return 1

def main():
    # Input string
    toZumo.high()
    while True:
        time.sleep(4)
        input_string = '11101110'
    # Call the function to check if each character is '0' or '1'
        check_zero_one(input_string)

        time.sleep(4)
        input_string = '10101010'
    # Call the function to check if each character is '0' or '1'
        check_zero_one(input_string)
        print("Starting main loop...")

if __name__ == "__main__":
    main()
