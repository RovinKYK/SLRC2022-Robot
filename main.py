from robot import Robot
import time
robot = Robot()

#Helper functions for tasks

########################################################################

def main():
    print("hello world")
    test()
    pass
    
def test():
    ld = robot.left_dist_sensor.get_distance()
    rd = robot.right_dist_sensor.get_distance()
    print("Left distance = ", ld)
    print("Right distance = ", rd)
    print()
    time.sleep(1)

if __name__ == "__main__":
    main()
