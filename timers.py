from machine import Pin, UART, PWM, Timer
import time

# Define o pino onde o LED está conectado (neste caso, GP15)
led = Pin("LED", Pin.OUT)


#motor 
motor_en = PWM(Pin(20, Pin.OUT))
motor_fwd = Pin(21, Pin.OUT)
motor_rv = Pin(22, Pin.OUT)

#upper_motor_en = PWM(Pin(16, Pin.OUT))
#upper_motor_fwd = Pin(17, Pin.OUT)
#upper_motor_rv = Pin(18, Pin.OUT)


motor_en.freq(1000)

motor_en.duty_u16(0)
motor_fwd.low()
motor_rv.low()


#upper_motor_en.freq(1000)
#upper_motor_en.duty_u16()
#upper_motor_fwd.low()
#upper_motor_rv.low()



# Variável para armazenar o estado do LED
led_state = False
motor_flag = False 
flag = 1

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

def adv_callback():
     global advStop

     advStop = 1

def stay_callback():
    global stayStop

    stayStop = 1

def rt_callback():
    global rtStop

    rtStop = 1 

def wait_callback():
    global waitStop

    waitStop = 1    


ADV_timer  = Timer(1, mode=Timer.ONE_SHOT, period = 100, callback = adv_callback)
Stay_timer  = Timer(2, mode=Timer.ONE_SHOT, period = 1000, callback = stay_callback)
RT_timer   = Timer(3, mode=Timer.ONE_SHOT, period = 100, callback = rt_callback)
wait_timer  = Timer(4, mode=Timer.ONE_SHOT, period = 4000, callback = wait_callback)
# O loop principal pode estar vazio, já que o timer cuida de alternar o LED

def state_machine():

    global side_flag # se 1 significa que e o motor bracos laterais, else motor braco vertical 
    global first_Time 
    global input_flag 
    
    global upper_motor_state
    global side_motor_state


    global advStop
    global stayStop
    global rtStop
    global waitStop

    if side_flag ==0:  #Upper arm 
        if upper_motor_state == "UP":
            motor_en.duty_u16(65535)
            motor_fwd.high()
            motor_rv.low()
            ADV_timer.init()
            print("Loop no Up state")
            if advStop:
                upper_motor_state = "STAY"
                advStop = 0

        elif upper_motor_state == "STAY":
            motor_en.duty_u16(int((20/100)*65535))
            motor_fwd.high()
            motor_rv.low()
            Stay_timer.init()
            if stayStop:
                upper_motor_state = "DOWN"
                stayStop = 0

        elif upper_motor_state == "DOWN":
            motor_en.duty_u16(65535)
            motor_fwd.low()
            motor_rv.high()
            RT_timer.init()
            if rtStop:
                rtStop = 0
                upper_motor_state = "IDLE"
        
           
        elif upper_motor_state == "IDLE":
            motor_en.duty_u16(0)
            motor_fwd.low()
            motor_rv.low()
            wait_timer.init()

            if waitStop:
                first_Time = True
                input_flag = 1
                waitStop = 0
    


while True:
    
    state_machine()

    if input_flag:
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
        side_flag = 1 
        first_Time = False
        side_motor_state = "UP"
        led.toggle()

    if first_Time and command == "3":
        print("Upper Arm Active")
        side_flag = 0 
        first_Time = False
        upper_motor_state = "UP"
        led.toggle()