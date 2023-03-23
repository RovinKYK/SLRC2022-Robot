from robot import Robot
import time
import RPi.GPIO as IO
robot = Robot()

#Helper functions for tasks

########################################################################

def main():
<<<<<<< HEAD
    test_IR_Sensor_Attay()
=======
    test_motor()
>>>>>>> e7731df74b4b35c4ca2250f5adba807a2a2a28ba
    
def test_distance_sensors():
    while True:
        ld = robot.left_dist_sensor.get_distance()
        rd = robot.right_dist_sensor.get_distance()
        print("Left distance = ", ld)
        print("Right distance = ", rd)
        print()
        time.sleep(1)

def test_Single_IR():
    while True:
        print(robot.left_IR1.detects_white())
        time.sleep(0.1)

def test_IR_Sensor_Attay():
    while True:
        print(robot.left_IR1.detects_white(),
            robot.left_IR2.detects_white(),
            robot.left_IR3.detects_white(),
            robot.left_IR4.detects_white(),
            robot.right_IR1.detects_white(),
            robot.right_IR2.detects_white(),
            robot.right_IR3.detects_white(),
            robot.right_IR4.detects_white())
        time.sleep(0.1)

def test_encoders():
    a=0
    robot.encoder.reset_distance()
    while True:
        b=robot.encoder.get_distance_moved()
        print("AA")
        print(b-a, b)
        a=b
        time.sleep(5)

def test_colour_sensor():
    while True:
        robot.colour_sensor.detects_colour()
        time.sleep(1)

if __name__ == "__main__":
    main()

def test_motor():
    robot.move_forward(70)