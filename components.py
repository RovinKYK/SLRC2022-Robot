import RPi.GPIO as IO
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