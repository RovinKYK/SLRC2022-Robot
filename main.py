from robot import Robot
import time
import RPi.GPIO as IO
robot = Robot()

#Helper functions for tasks

########################################################################

def main():
    print("hello world")
<<<<<<< HEAD
    IO.setmode(IO.BOARD)
    IO.setup(40, IO.OUT)
    IO.output(40, IO.HIGH)

    test_IR_Sensors()
=======
    test_encoders()
>>>>>>> 3f5d24a42a54575096205cef284ae09da1bca800
    
def test_distance_sensors():
    while True:
        ld = robot.left_dist_sensor.get_distance()
        rd = robot.right_dist_sensor.get_distance()
        print("Left distance = ", ld)
        print("Right distance = ", rd)
        print()
        time.sleep(1)

def test_IR_Sensors():
    while True:
        print(robot.left_IR1.detects_white(),
            robot.left_IR2.detects_white(),
            robot.left_IR3.detects_white(),
            robot.left_IR4.detects_white(),
            robot.right_IR1.detects_white(),
            robot.right_IR2.detects_white(),
            robot.right_IR3.detects_white(),
            robot.right_IR4.detects_white())
        time.sleep(1)

def test_encoders():
    while True:
        print(robot.encoder.get_distance_moved())
        time.sleep(5)

if __name__ == "__main__":
    main()
