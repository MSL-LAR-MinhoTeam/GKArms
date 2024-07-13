from machine import Pin, UART, PWM, Timer
import time
import utime
import _thread
import sys

# Define o pino onde o LED está conectado (neste caso, GP15)
led = Pin("LED", Pin.OUT)

uart = UART(1, baudrate=115200)

time_to_up = 500
time_to_down = 150
time_stay = 1200 - time_to_up - time_to_down

current_time = utime.ticks_ms()
old_time = current_time

#motor upper arm 
upper_motor_en = PWM(Pin(16, Pin.OUT))
upper_motor_fwd = Pin(17, Pin.OUT)
upper_motor_rv = Pin(18, Pin.OUT)

upper_motor_en.freq(1000)
upper_motor_en.duty_u16(0)
upper_motor_fwd.low()
upper_motor_rv.low()



side_motor_en = PWM(Pin(20, Pin.OUT))
side_motor_fwd = Pin(21, Pin.OUT)
side_motor_rv = Pin(22, Pin.OUT)

side_motor_en.freq(1000)
side_motor_en.duty_u16(0)
side_motor_fwd.low()
side_motor_rv.low()



# Variável para armazenar o estado do LED
led_state = False
motor_flag = False 
upper_motor_state = False
side_flag = False 
flag = 1
input_flag = True
first_Time = True
command = "null" 

# Função que será chamada pelo timer para alternar o estado do LED
def toggle_led(timer):
    global led_state
    global motor_flag

    print("Callback")

    led_state = not led_state
    motor_flag = not motor_flag
    led.value(led_state)
    
    #led.toggle()

def reset_cycle():
    global motor_flag

    motor_flag = 0 
    

# Configura o timer para chamar a função toggle_led a cada 1 segundo (1000 ms)

#timer1 = Timer()
#timer1.init(period=1000, mode=Timer.PERIODIC, callback=toggle_led)



#ADV_timer  = Timer( mode=Timer.ONE_SHOT, period = 100, callback = adv_callback)
#Stay_timer  = Timer( mode=Timer.ONE_SHOT, period = 1000, callback = stay_callback)
#RT_timer   = Timer( mode=Timer.ONE_SHOT, period = 100, callback = rt_callback)
#wait_timer  = Timer( mode=Timer.ONE_SHOT, period = 4000, callback = wait_callback)
# O loop principal poe estar vazio, já que o timer cuida de alternar o LED

def state_machine():

    global side_flag # se 1 significa que e o motor bracos laterais, else motor braco vertical 
    global first_Time 
    global input_flag 
    
    global upper_motor_state
    global side_motor_state

    global command

    global advStop
    global stayStop
    global rtStop
    global waitStop


    global current_time
    global old_time



    if side_flag == 1:  #Right arm 
        if side_motor_state == "UP":
            print("aqui1")
            side_motor_en.duty_u16(65535)
            side_motor_fwd.high()
            side_motor_rv.low()
            time.sleep_ms(20)
            print("Loop no Up state")
            
            side_motor_state = "STAY"

        elif side_motor_state == "STAY":
            side_motor_en.duty_u16(int((20/100)*65535))
            side_motor_fwd.high()
            side_motor_rv.low()
            time.sleep_ms(1000)
            print("Stay")
            side_motor_state = "DOWN"
        
        elif side_motor_state == "DOWN":
            side_motor_en.duty_u16(65535)
            side_motor_fwd.low()
            side_motor_rv.high()
            time.sleep_ms(40)
            print("Down")
            side_motor_state = "IDLE"
        
           
        elif side_motor_state == "IDLE":
            side_motor_en.duty_u16(0)
            side_motor_fwd.low()
            side_motor_rv.low()
            print("Start Iddle")
            time.sleep_ms(4000)
            print("End Iddle")
            first_Time = True
            input_flag = 1
            command = "null"

    if side_flag ==2:  #Left arm 
        if upper_motor_state == "UP":
            print("aqui1")
            side_motor_en.duty_u16(65535)
            side_motor_fwd.low()
            side_motor_rv.high()
            time.sleep_ms(5)
            print("Loop no Up state")
            
            upper_motor_state = "STAY"

        elif upper_motor_state == "STAY":
            side_motor_en.duty_u16(int((20/100)*65535))
            side_motor_fwd.low()
            side_motor_rv.high()
            time.sleep_ms(1000)
            print("Stay")
            upper_motor_state = "DOWN"
        
        elif upper_motor_state == "DOWN":
            side_motor_en.duty_u16(65535)
            side_motor_fwd.high()
            side_motor_rv.low()
            time.sleep_ms(40)
            print("Down")
            upper_motor_state = "IDLE"
        
           
        elif upper_motor_state == "IDLE":
            side_motor_en.duty_u16(0)
            side_motor_fwd.low()
            side_motor_rv.low()
            print("Start Iddle")
            time.sleep_ms(4000)
            print("End Iddle")
            first_Time = True
            input_flag = 1
            command = "null"
    
    if side_flag ==3:  #Upper arm 
        if upper_motor_state == "UP":
            upper_motor_en.duty_u16(int(65535/2))
            upper_motor_fwd.high()
            upper_motor_rv.low()
            current_time = utime.ticks_ms()
            if current_time - old_time > time_to_up:
                old_time = current_time
                upper_motor_state = "STAY"
                print("State STAY")
        elif upper_motor_state == "STAY":
            upper_motor_en.duty_u16(int(int((20/100)*65535)/2))
            upper_motor_fwd.high()
            upper_motor_rv.low()
            current_time = utime.ticks_ms()
            if current_time - old_time > time_stay:
                old_time = current_time
                upper_motor_state = "DOWN"
                print("State DOWN")
        elif upper_motor_state == "DOWN":
            upper_motor_en.duty_u16(int(65535/2))
            upper_motor_fwd.low()
            upper_motor_rv.high()
            current_time = utime.ticks_ms()
            if current_time - old_time > time_to_down:
                old_time = current_time
                upper_motor_state = "WAIT"
                print("State WAIT")
        elif upper_motor_state == "WAIT":
            upper_motor_en.duty_u16(int((10/100)*int(65535/2)))
            upper_motor_fwd.high()
            upper_motor_rv.low()
            current_time = utime.ticks_ms()
            if current_time - old_time > 4000:
                old_time = current_time
                upper_motor_state = "IDLE"
                command = "0"
                print("State IDLE")
        elif upper_motor_state == "IDLE":
            upper_motor_en.duty_u16(0)
            upper_motor_fwd.low()
            upper_motor_rv.low()
            first_Time = True
            input_flag=1
            command = "null"
        


while True:
    
    state_machine()

    if input_flag:
        led.toggle()
        command = input("Command:")
        input_flag = 0
        #timer2.init()

    if first_Time and command == "1":
        print("Right Arm Active")
        side_flag = 1 
        first_Time = False 
        side_motor_state = "UP"
        led.toggle()
    
    if first_Time and command == "2":
        print("Left Arm Active")
        side_flag = 2 
        first_Time = False 
        side_motor_state = "UP"
        led.toggle()


    if first_Time and command == "3":
        print("Upper Arm Active")
        side_flag = 3 
        current_time = utime.ticks_ms()
        old_time = current_time
        first_Time = False
        upper_motor_state = "UP"
        led.toggle()



