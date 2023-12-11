# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""CircuitPython Essentials NeoPixel example"""
import time
import board
from rainbowio import colorwheel
import neopixel
import digitalio
import pwmio
import binascii #import libraries that are needed to run the code
import busio

from adafruit_motor import motor #Imports a function from the adafruit_motor library
from dabble import Dabble

dabble = Dabble(board.GP0, board.GP1, debug=True) #defines hardware and attaches it to a pin

# ** Change this value to connnect the DIN wire to a different pin on the Pico
pixel_pin = board.GP2

# ** Change this number to be the number of LEDs on your strips
num_pixels = 10

# This line initialized the library used to control the neopixel strip
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False)

# Different colors are made by mixing different amounts of
# Red, Green and Blue light.  The color wheel for light
# is different from mixing paint!
#
# Here are some RGB values for some common colors.
# 0 == LED off and 255 == full brightness
RED    = (255,   0,   0) # 100% red,   0% green, 0% blue
GREEN  = (  0, 255,   0) #   0% red, 100% green, 0% blue
BLUE   = (  0,   0, 255) # 100% blue
CYAN   = (  0, 255, 255) #   0% red, 100% green, 100% blue
YELLOW = (255, 150,   0) # 100% red,  55% green, 0% blue
WHITE  = (100, 100, 100) # 100% of all colors
BLACK  = (  0,   0,   0) # 0% of all colors (turns the LED off)

# ** Can you figure out the values for these colors?
#LIGHTBLUE = (?, ?, ?)
#LIGHTPINK = (?, ?, ?)
#ORANGE = (?, ?, ?)
#CYAN = (?, ?, ?)
#PURPLE = (?, ?, ?)
#MAGENTA = (?, ?, ?)

# ** Make your own colors and see what happens!
#MYCOLOR1 RGB(?, ?, ?)
#MYCOLOR2 RGB(?, ?, ?)
#MYCOLOR3 RGB(?, ?, ?)
#MYCOLOR4 RGB(?, ?, ?)


left_motor_forward = board.GP12 #initializes the variable left_motor_forward and attachees it to GP12
left_motor_backward = board.GP13#initializes the variable left_motor_backward and attachees it to GP13
right_motor_forward = board.GP14
right_motor_backward = board.GP15

pwm_La = pwmio.PWMOut(left_motor_forward, frequency=10000) #tells the controller that the motor is an output
pwm_Lb = pwmio.PWMOut(left_motor_backward, frequency=10000) #tells the controller that the motor is an output
pwm_Lc = pwmio.PWMOut(right_motor_forward, frequency=10000)
pwm_Ld = pwmio.PWMOut(right_motor_backward, frequency=10000)

left_Motor = motor.DCMotor(pwm_La, pwm_Lb) #Configuration line (it is required)
left_Motor_speed = 0 # Initiates Variable for the left motor speed
right_Motor = motor.DCMotor(pwm_Lc, pwm_Ld)
right_Motor_speed = 0

def move_forward():
    left_Motor_speed = 1 #Makes left wheel forward
    left_Motor.throttle = left_Motor_speed
    right_Motor_speed = 1 #Makes right motor go forward
    right_Motor.throttle = right_Motor_speed

def move_backward():
    left_Motor_speed = -1 #Makes left wheel backward
    left_Motor.throttle = left_Motor_speed
    right_Motor_speed = -1 #Makes right motor go backward
    right_Motor.throttle = right_Motor_speed

def turn_left():
    left_Motor_speed = -1 #Makes left wheel backward
    left_Motor.throttle = left_Motor_speed
    right_Motor_speed = 1 #Makes right motor go forward
    right_Motor.throttle = right_Motor_speed

def turn_right():
    left_Motor_speed = 1 #Makes left wheel forward
    left_Motor.throttle = left_Motor_speed
    right_Motor_speed = -1 #Makes right motor go backward
    right_Motor.throttle = right_Motor_speed

def stop():
    left_Motor_speed = 0 #Makes left wheel forward
    left_Motor.throttle = left_Motor_speed
    right_Motor_speed = 0 #Makes right motor go backward
    right_Motor.throttle = right_Motor_speed


# Put Bluetooth processing While loop here
while True:
    message = dabble.read_message()
    if (message != None):
        print("Message: " + str(message))
        # Implement tank steering on a 2 wheeled robot
        if (message.up_arrow_pressed):
            print("Move both motors forward")
            move_forward()
        elif (message.down_arrow_pressed):
            print("Move both motors backward")
            move_backward()
        elif (message.right_arrow_pressed):
            print("Move left motor forward and right motor backward")
            turn_right()
        elif (message.left_arrow_pressed):
            print("Move left motor backward and right motor forward")
            turn_left()
        elif (message.no_direction_pressed):
            print("Stop both motors")
            stop()
        else:
            print("Something crazy happened with direction!")

        if (message.triangle_pressed):
            print("Raise arm")
        elif (message.circle_pressed):
            print("Lower arm")
        elif (message.square_pressed):
            print("Squirt water")
        elif (message.circle_pressed):
            print("Fire laser")
        elif (message.start_pressed):
            print("Turn on LED")
        elif (message.select_pressed):
            print("Do victory dance")
        elif (message.no_action_pressed):
            print("No action")
        else:
            print("Something crazy happened with action!")
"""

OLD code for testing motors
while True:
    left_Motor_speed = 1 #Makes the left wheel go forward
    left_Motor.throttle = left_Motor_speed
    pixels.fill(RED)
    pixels.show()
    time.sleep(2)

    left_Motor_speed = -1 #Makes the left wheel go backward
    left_Motor.throttle = left_Motor_speed
    pixels.fill(BLACK)
    pixels.show()

    time.sleep(2) #tells me how long command goes on
    right_Motor_speed = 1 #Makes the right wheel go forward
    right_Motor.throttle = right_Motor_speed
    time.sleep(2)
    right_Motor_speed = -1 #Makes the right wheel go backward
    right_Motor.throttle = right_Motor_speed
    time.sleep(2)


OLD code for testing the neopixels
##############################################################################
# This is the main body of your code
while True:

    # Clear out the pixel strip
    pixels.fill(BLACK)

    # ** You can make changes below here

    # print() shows a message in the Serial Monitor.
    # Open it using the "Serial" icon at the top of the Mu Editor
    print("Showing colors");

    # Setting pixel[N] to a color sets one pixel at position N to a specific color
    # Note that the first pixel starts at zero!

    # Set the first 5 pixels to a specific color
    pixels[0] = RED
    pixels[1] = BLUE
    pixels[2] = GREEN
    pixels[3] = BLACK
    pixels[4] = WHITE

    # pixels.show() must be called for any changes with SET() to take effect.
    pixels.show()

    # time.sleep() pauses the program for the specified number of seconds.
    # You can use a decimal to pause for less than a second, e.g. time.sleep(.5)
    time.sleep(4)

    # pixels.fill() sets every LED to the same color
    print ("Turning off all LEDs on the strip");
    pixels.fill(BLACK)
    pixels.show()
    time.sleep(2)

    print("Seting the strip to a solid color")
    pixels.fill(RED)
    pixels.show()
    time.sleep(2)

    print("color_chase(BLUE): moves red across the strip")
    color_chase(BLUE, 0.1)  # Increase the number to slow down the color chase

    #print("theater_chase(): make lights run up the strip")
    #theater_chase(RED, .1)

    #print("theater_chase2(): make lights run up the strip")
    #theater_chase2(CYAN, YELLOW, .1)

    #print("theater_chase3(): make lights run up the strip")
    #theater_chase3(RED, WHITE, BLUE, .1)

    #print("theater_chase_rainbow(): make lights run up the strip")
    #theater_chase_rainbow(.05)

    #print("rainbow(): LEDs cycle through the colors one at a time.")
    #rainbow(.02)

    #print("rainbow_cycle(): fade different colors with 20ms between colors")
    #rainbow_cycle(.02)
"""




