from robot import Robot
import time
import RPi.GPIO as IO
from components import *
robot = Robot()

#Helper functions for tasks

########################################################################

def main():
    #test_distance_sensors()
    roobt=Robot()
    robot.move_distance(15)
    robot.line_follow()
    while colour_sensor.detects_colour()!='Blue':
        robot.stop()
        break
    robot.run_line_maze_arena()
    robot.move_distance(15)
    robot.line_follow()
    while colour_sensor.detects_colour()!='White':
        robot.stop()
        break
    robot.run_cave_arena()
    robot.line_follow()
    while colour_sensor.detects_colour()!='White':
        robot.stop()
        break
    robot.arrow_follow()
    while colour_sensor.detects_colour()!='Blue':
        robot.stop()
        break
    robot.line_follow()
    while colour_sensor.detects_colour()!='White':
        robot.stop()
        break

def test_distance_sensors():
    while True:
        a=robot.side_left_dist_sensor.get_distance()
        b=robot.front_left_dist_sensor.get_distance()
        c=robot.front_middle_dist_sensor.get_distance()
        d=robot.front_right_dist_sensor.get_distance()
        e=robot.side_right_dist_sensor.get_distance()
        print("Distances")
        print(a," ",c,d,e)
        print()
        time.sleep(1)

def test_Single_IR():
    while True:
        print(robot.middle_IR.detects_white())
        time.sleep(0.1)

def test_IR_Sensor_Attay():
    while True:
        print(robot.outer_left_IR.detects_white(),
            robot.inner_left_IR.detects_white(),
            robot.middle_IR.detects_white(),
            robot.inner_right_IR.detects_white(),
            robot.outer_right_IR.detects_white())
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
def test_motor():
    robot.move_forward(70)

if __name__ == "__main__":
    main()

