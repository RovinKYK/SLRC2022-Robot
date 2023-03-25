from robot import Robot
import time
import RPi.GPIO as IO

robot = Robot()
#Helper functions for tasks

########################################################################

def test_motor():
    print("test1")
    try:
        for i in range(20,21):
            print(i)
            robot.left_motor.move_forward(i)
            print("test1")
            robot.right_motor.move_forward(i)
            time.sleep(20)
            print("done")
    except Exception as e:
        print(e)
    finally:
        robot.left_motor.stop()
        robot.right_motor.stop()
        print("All done")

def main():
    # test_distance_sensors()
    # while not robot.outer_left_IR.detects_white() and not robot.outer_right_IR.detects_white():
    #     robot.move_forward(25)
    # robot.stop()
    # robot.initial_line_follow(25)

    #robot.turn_left(21,1)
    #robot.line_follow()
    #test_IR_Sensor_Attay()
    #test_motor()
    # print(robot.initial_line_follow(22))
    # robot.run_line_maze_arena()
    #test_colour_sensor()
    #robot.run_line_maze_arena()
    test_compass()

def test_compass():
    while True:
        print(robot.compass.get_true_bearing())

def test_distance_sensors():
    while True:
        a=robot.side_left_dist_sensor.get_distance()
        b=robot.front_left_dist_sensor.get_distance()
        c=robot.front_middle_dist_sensor.get_distance()
        d=robot.front_right_dist_sensor.get_distance()
        e=robot.side_right_dist_sensor.get_distance()
        print("Distances")
        print(a,b,c,d,e)
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
        time.sleep(0.1)
#def test_motor():
    #robot.move_forward(70)

if __name__ == "__main__":
    main()

