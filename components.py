import RPi.GPIO as IO
import time
from i2c_hmc5883l import HMC5883
 

class Compass:
    def __init__(self):
        self.sensor = HMC5883(gauss=4)
        self.sensor.set_declination(-2, 0)

    def set_initial_bearing(self):
        self.initial_bearing = self.get_true_bearing()

    def get_bearing(self):
        relative_bearing = self.get_true_bearing() - self.initial_bearing
        if relative_bearing < 0:
            relative_bearing = 360 + relative_bearing
            
        return relative_bearing

    def get_true_bearing(self):
        deg, min = self.sensor.get_heading()
        return deg

class IRSensor:
    def __init__(self, pin):
        self.pin = pin
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(pin, IO.IN)

    def detects_white(self):
        return int(not IO.input(self.pin))

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
        IO.setmode(IO.BCM)
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
        start_speed = self.speed
        for speed in range(start_speed, self.min_speed,-1):
            self.pwm.ChangeDutyCycle(speed)
            self.speed = speed
            time.sleep(self.interval)

        self.stop()

    def move_forward(self,speed):
        IO.output(self.forward_pin, IO.LOW)
        IO.output(self.backward_pin, IO.HIGH)
        self.pwm.ChangeDutyCycle(speed)

    def move_backward(self,speed):
        IO.output(self.forward_pin, IO.HIGH)
        IO.output(self.backward_pin, IO.LOW)
        self.pwm.ChangeDutyCycle(speed)

    def stop(self):
        self.pwm.ChangeDutyCycle(0)
        self.speed = 0

    def shutdown(self):
        self.pwm.stop()


class DistanceSensor:
    def __init__(self, trig_pin, echo_pin):
        self.trig_pin = trig_pin
        self.echo_pin = echo_pin

        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        IO.setup(self.trig_pin, IO.OUT)
        IO.setup(self.echo_pin, IO.IN)

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
    def __init__(self, en_pin1, en_pin2, sel_pin1, sel_pin2, output_pin):
        self.en_pin1 = en_pin1
        self.en_pin2 = en_pin2
        self.sel_pin1 = sel_pin1
        self.sel_pin2 = sel_pin2
        self.output_pin = output_pin
        
        self.lower_range = 300
        self.upper_range = 350
        self.num_cycles = 10      

        IO.setmode(IO.BCM)
        IO.setwarnings(False)
        IO.setup(self.output_pin,IO.IN, pull_up_down=IO.PUD_UP)
        IO.setup(self.en_pin1,IO.OUT)
        IO.setup(self.en_pin2,IO.OUT)
        IO.setup(self.sel_pin1,IO.OUT)
        IO.setup(self.sel_pin2,IO.OUT)

        IO.output(self.en_pin1,IO.HIGH)
        IO.output(self.en_pin2,IO.LOW)

    def detects_colour(self):
        #time.sleep(3)
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
        
        print(red,green,blue)
        
        if red>3800 and green>3800 and blue>3800:
            print("white")
            return "white"
        if red<2900 and green<2900 and blue<2900:
            print("black")
            return "black"
        if blue>3800:
            print("blue")
            return "blue"
        if green>2900 and blue>2900:
            print("green")
            return "green"
        if red>3800:
            print("red")
            return "red"
        else: 
            print("none")
            return "none"
        

class Encoder:
    def __init__(self, pin):
        self.pin = pin
        self.debounce_time = 0.035
        self.distance_per_count = 2.522 * 10

        IO.setmode(IO.BCM)
        IO.setup(pin, IO.IN)

        self.counter = 0
        self.last_time = time.time()

        IO.add_event_detect(pin, IO.RISING)
        IO.add_event_callback(pin, self.increment)

    def increment(self, channel):
        if ((time.time() - self.last_time) > self.debounce_time):
            self.counter += 1
            self.last_time = time.time()

    def reset_distance(self):
        self.counter = 0

    def get_distance_moved(self):
        return self.distance_per_count * self.counter

class Encoder2:
    def __init__(self, pin):
        self.pin = pin
        self.count = 0
        self.prev_state = IO.input(pin)
        self.distance_per_count = 2.522 * 10

        IO.setmode(IO.BCM)
        IO.setup(pin, IO.IN, pull_up_down=IO.PUD_UP)
        IO.add_event_detect(pin, IO.BOTH, callback=self.increment)

    def increment(self, channel):
        self.state = IO.input(self.pin)
        if self.prev_state == IO.HIGH and self.state == IO.LOW:
            count += 1
        self.prev_state = self.state

    def reset_distance(self):
        self.counter = 0

    def get_distance_moved(self):
        return self.distance_per_count * self.counter


class PushButton():
    def __init__(self, pin):
        self.pin = pin
        IO.setwarnings(False)
        IO.setmode(IO.BCM)
        IO.setup(pin, IO.IN)

    def button_pressed(self):
        return int(IO.input(self.pin))
