from components import *
class Robot:
    def __init__(self):
        left_motor = Motor(1,1,1)
        right_motor = Motor(1,1,1)

        compass = Compass()
        encoder = Encoder()
        colour_sensor = ColourSensor()
        
        front_dist_sensor = DistanceSensor()
        left_dist_sensor = DistanceSensor()
        right_dist_sensor = DistanceSensor()

        left_IR1 = IRSensor(1)
        left_IR2 = IRSensor(1)
        left_IR3 = IRSensor(1)
        left_IR4 = IRSensor(1)
        right_IR1 = IRSensor(1)
        right_IR2 = IRSensor(1)
        right_IR3 = IRSensor(1)
        right_IR4 = IRSensor(1)


        



        