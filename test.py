from machine import Pin, UART, PWM, Timer
import time
import utime
import _thread
import sys


upper_motor_en = PWM(Pin(20, Pin.OUT))
upper_motor_fwd = Pin(21,Pin.OUT)
upper_motor_rv = Pin(22, Pin.OUT)

upper_motor_en.freq(1000)
upper_motor_en.duty_u16(0)
upper_motor_fwd.low()
upper_motor_rv.low()

led = Pin("LED", Pin.OUT)

while True:

    led.toggle()
    upper_motor_en.duty_u16(65535)
    upper_motor_fwd.high()
    upper_motor_rv.low()


