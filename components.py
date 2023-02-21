import RPi.GPIO as IO
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


class IRsenor:
    def __init__(self, pin):
        self.pin = pin
        IO.setwarnings(False)
        IO.setmode(IO.BOARD)
        IO.setup(pin, IO.IN)

    def detects_white(self):
        return not IO.input(self.pin)

