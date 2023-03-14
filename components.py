import RPi.IO as IO
import time
from qmc5883l import *

class Compass:
    def __init__(self):
        self.sensor = QMC5883L(output_data_rate=ODR_100HZ)
        self.sensor.declination = -2.11
        self.initial_bearing

    def set_initial_bearing(self):
        self.initial_bearing = self.__get_true_bearing()

    def get_bearing(self):
        relative_bearing = self.__get_true_bearing() - self.initial_bearing
        if relative_bearing < 0:
            relative_bearing = 360 + relative_bearing
            
        return relative_bearing

    def get_true_bearing(self):
        return self.sensor.get_bearing()


class IRSensor:
    def __init__(self, pin):
        self.pin = pin
        IO.setwarnings(False)
        IO.setmode(IO.BOARD)
        IO.setup(pin, IO.IN)

    def detects_white(self):
        return not IO.input(self.pin)


class Motor:
    def __init__(self, en_pin, forward_pin, backward_pin):
        self.en_pin = en_pin
        self.forward_pin = forward_pin
        self.backward_pin = backward_pin

        self.frequency = 256
        self.speed = 0.0
        self.interval = 0.05
        self.min_speed = 70

        IO.setwarnings(False)
        IO.setmode(IO.BOARD)
        IO.setup(en_pin, IO.OUT)
        IO.setup(forward_pin, IO.OUT)
        IO.setup(backward_pin, IO.OUT)

        self.pwm = IO.PWM(en_pin, self.frequency)
        self.pwm.start(self.speed)

    def move_forward_smooth(self, max_speed):
        IO.output(self.forward_pin, IO.LOW)
        IO.output(self.backward_pin, IO.HIGH)
        
        for speed in range(70,max_speed):
            self.pwm.ChangeDutyCycle(speed)
            self.speed = speed
            time.sleep(self.interval)

    def move_backward_smooth(self, max_speed):
        IO.output(self.forward_pin, IO.HIGH)
        IO.output(self.backward_pin, IO.LOW)
        
        for speed in range(70,max_speed):
            self.pwm.ChangeDutyCycle(speed)
            self.speed = speed
            time.sleep(self.interval)

    def stop_smooth(self):
        for speed in range(speed,70,-1):
            self.pwm.ChangeDutyCycle(speed)
            self.speed = speed
            time.sleep(self.interval)

        self.stop()

    def move_forward(self,speed):
        IO.output(self.forward_pin, IO.LOW)
        IO.output(self.backward_pin, IO.HIGH)
        self.motorPWM.ChangeDutyCycle(speed)

    def move_backward(self,speed):
        IO.output(self.forward_pin, IO.HIGH)
        IO.output(self.backward_pin, IO.LOW)
        self.motorPWM.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)

    def shutdown(self):
        self.pwm.stop()


class DistanceSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        IO.setup(self.trig_pin, IO.OUT)
        IO.setup(self.echo_pin, IO.IN)
        IO.setmode(IO.BOARD)

    def get_distance(self):
        IO.output(self.trig_pin, True)
        time.sleep(0.00001)
        IO.output(self.trig_pin, False)
    
        StartTime = time.time()
        StopTime = time.time()
        
        while IO.input(self.echo_pin) == 0:
            StartTime = time.time()
    
        while IO.input(self.echo_pin) == 1:
            StopTime = time.time()
    
        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2
    
        return distance


class ColourSensor:
    def __init__(self, sel_pin1, sel_pin2, output_pin):
        self.sel_pin1 = sel_pin1
        self.sel_pin2 = sel_pin2
        self.output_pin = output_pin
        
        self.num_cycles = 10

        IO.setmode(IO.BOARD)
        IO.setup(self.output_pin,IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.sel_pin1,IO.OUT)
        IO.setup(self.sel_pin2,IO.OUT)

    def detects_colour(self):
        IO.output(self.sel_pin1,IO.LOW)
        IO.output(self.sel_pin2,IO.LOW)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(self.num_cycles):
            IO.wait_for_edge(self.output_pin, IO.FALLING)
        duration = time.time() - start 
        red  = self.num_cycles / duration   
    
        IO.output(self.sel_pin1,IO.LOW)
        IO.output(self.sel_pin2,IO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(self.num_cycles):
            IO.wait_for_edge(self.output_pin, IO.FALLING)
        duration = time.time() - start
        blue = self.num_cycles / duration
        
        IO.output(self.sel_pin1,IO.HIGH)
        IO.output(self.sel_pin2,IO.HIGH)
        time.sleep(0.3)
        start = time.time()
        for impulse_count in range(self.num_cycles):
            IO.wait_for_edge(self.output_pin, IO.FALLING)
        duration = time.time() - start
        green = self.num_cycles / duration
        
        if green<7000 and blue<7000 and red>12000:
            return 'Red'
        elif red<12000 and  blue<12000 and green>12000:
            return 'Green'
        elif green<7000 and red<7000 and blue>12000:
            return 'Blue'
        else:
        #elif red>10000 and green>10000 and blue>10000:
            return False


    class Encoder:
        '''Dummy class'''
        def __init__(self):
            self.distance = 0

        def reset(self):
            self.distance = 0

        def get_distance_moved(self):
            return self.distance
    
