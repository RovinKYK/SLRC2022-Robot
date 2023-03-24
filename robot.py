from turtle import color
from components import *

class Robot:
    def __init__(self):
        '''self.left_motor = Motor(15,16)
        self.right_motor = Motor(11,13)'''

        #self.compass = Compass(3,5)
        #self.colour_sensor = ColourSensor(12,33,27,29,31)
        #self.encoder = Encoder(7)
        #self.push_button = PushButton()
        self.inner_left_IR = IRSensor(27)

        '''self.front_middle_dist_sensor = DistanceSensor(38,32)
        self.front_middle_dist_sensor = DistanceSensor(38,32)
        #self.front_left_dist_sensor = DistanceSensor(40,) #3=28
        self.front_right_dist_sensor = DistanceSensor(37,26)
        self.side_left_dist_sensor = DistanceSensor(36,24)
        self.side_right_dist_sensor = DistanceSensor(35,23)
        '''
        '''

        self.middle_IR = IRSensor(10)
        self.inner_left_IR = IRSensor(8)
        self.inner_right_IR = IRSensor(7)
        self.outer_left_IR = IRSensor(18)
        self.outer_right_IR = IRSensor(19)

        #self.servo_motor
        self.curr_dir=0 # 0=north, 1=east, 2=south, 3=west   This will be useful for the grid areas'''

    def move_forward(self, speed):
        self.left_motor.move_forward(speed)
        self.right_motor.move_forward(speed)

    def move_backward(self, speed):
        self.left_motor.move_backward(speed)
        self.right_motor.move_backward(speed)

    def move_distance(self, distance, speed):
        self.left_motor.move_forward(speed)
        self.right_motor.move_forward(speed)

    def turn_left(self): # 90 degree turn
        self.left_motor.move_backward(70)
        self.right_motor.move_forward(70)
        time.sleep(1.5)
        self.left_motor.stop()
        self.right_motor.stop()

    def turn_right(self): # 90 degree turn
        self.left_motor.move_forward(70)
        self.right_motor.move_backward(70)
        time.sleep(1.5)
        self.left_motor.stop()
        self.right_motor.stop()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def reverse(self):
        self.left_motor.move_backward(70)
        self.right_motor.move_backward(70)
        time.sleep(1.5)
        self.left_motor.stop()
        self.right_motor.stop()

    def line_follow(self, speed=80):
        while True:
            # read sensor values
            inner_left = self.left_IR2.detects_white()
            inner_right = self.right_IR2.detects_white()
            middle = self.middle_IR.detects_white()

            # adjust motors based on sensor values
            if inner_left and not inner_right:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            if not inner_left and inner_right:
                self.left_motor.move_forward(speed)
                self.right_motor.move_backward(speed)
            if not inner_left and not inner_right:
                self.move_forward(speed)
            if (inner_left and inner_right) or middle:
                self.stop()
                break
    def arrow_follow(self, speed=80):
        while True:
            # read sensor values
            inner_left = self.left_IR2.detects_white()
            inner_right = self.right_IR2.detects_white()
            color = self.colour_sensor.detects_colour()

            if color == 'Blue':
                self.stop()
                break  
            # adjust motors based on sensor values
            if inner_left and not inner_right:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            elif not inner_left and inner_right:
                self.left_motor.move_forward(speed)
                self.right_motor.move_backward(speed)
            else:
                self.move_forward(speed)
        
    def maze_go(self,direction):
        diff=direction-self.curr_dir
        if diff==1 or diff==-3:
            self.turn_right()
        if diff==-1 or diff==3:
            self.turn_left()
        if diff==2 or diff==-2:
            self.turn_right()
            self.turn_right()
        self.encoder.reset()
        self.line_follow(80)

        # Move till the robot is in middle of the junction. calibrate exact values later
        self.move_forward(80)
        time.sleep(0.5)
        self.stop()
        self.curr_dir=direction
        return (self.encoder.get_distance_moved//35)      # returns the number of junctions travelled

    def is_visited(self,visited,current):      # this step won't be nessesary if there are no cycles in the maze
        destination=current+(-4 if self.curr_dir==0 else 1 if self.curr_dir==1 else 4 if self.curr_dir==2 else -1)
        if destination in visited:
            return True
        return False

    def run_line_maze_arena(self):
        # assuming that we start on middle of blue box facing west
        directions=['north','east','south','west']
        self.curr_dir=3
        visited=[20]
        pathToLast=[]       #path to the last turning point in reverse
        turningPoints=[]    #this is a stack of turning points
        current=20
        while True:
            # check for finish line
            color = self.colour_sensor.detects_colour()
            if color == 'Red':
                self.stop()
                break
            paths=[]        
            # check the available paths
            self.turn_right()
            self.curr_dir=(self.curr_dir+1)%4
            if self.left_IR1.detects_white() or self.right_IR1.detects_white():
                if not self.is_visited(visited,current,self.curr_dir):
                    paths.append(self.curr_dir)
            self.turn_left()
            self.curr_dir=(self.curr_dir-1)%4
            if self.left_IR1.detects_white() or self.right_IR1.detects_white():
                if not self.is_visited(visited,current,self.curr_dir):
                    paths.append(self.curr_dir)
            self.turn_left()
            self.curr_dir=(self.curr_dir-1)%4
            if self.left_IR1.detects_white() or self.right_IR1.detects_white():
                paths.append(self.curr_dir)

            if len(paths)==0: # if dead end, go back to the last turning point
                for i in reversed(pathToLast):  
                    self.maze_go((i-2)%4)
                temp=turningPoints.pop()    # restore the state
                current=temp[0]
                pathToLast=temp[1]
                paths=temp[2]
                paths.pop(-1)            # remove the path that we just came from
            if len(paths)>0: # if there are paths available, go to the first one
                if len(paths)>1:    # if there are more than one paths available, save the current state as a turning point
                    turningPoints.append((current,pathToLast,paths))
                    pathToLast=[paths[-1]]
                self.maze_go(paths[-1])
                current=current+(-4 if self.curr_dir==0 else 1 if self.curr_dir==1 else 4 if self.curr_dir==2 else -1)
                visited.append(current)
        
    def run_cave_arena(self):
        # read sensor values
        color = self.colour_sensor.detects_colour()

        # Move forward 13 cm
        self.move_forward(80)
        time.sleep(0.5)
        self.stop()

        # Turn left
        self.turn_left()

        # Check for barriers
        while True:
            # Move forward
            self.move_forward(80)

            front_dist = self.front_dist_sensor.get_distance()
            if front_dist < 15:
                self.stop()
                # Avoid barrier by turning right
                self.turn_right()
                self.move_forward(80)
                time.sleep(0.5)
                self.turn_left()
                # Check for barriers again
                while True:
                    # Move forward
                    self.move_forward(80)

                    front_dist = self.front_dist_sensor.get_distance()
                    if front_dist < 15:
                        self.stop()
                        # Avoid barrier by turning left
                        self.turn_left()
                        self.move_forward(80)
                        time.sleep(0.5)
                        self.turn_right()

                    # Check for finish line
                    color = self.colour_sensor.detects_colour()
                    if color == 'White':
                        self.stop()
                        break

            # Check for finish line
            color = self.colour_sensor.detects_colour()
            if color == 'White':
                self.stop()
                break

        left_dist = self.left_dist_sensor.get_distance()
        right_dist = self.right_dist_sensor.get_distance()
        diff = left_dist - right_dist
        if diff > 0:
            self.turn_left()
            self.move_distance(left_dist - 55/2)
            self.turn_right()
        else:
            self.turn_right()
            self.move_distance(right_dist - 55/2)
            self.turn_left()
        
        self.move_distance(30)
    
    def run_7_segment_number_constructing_arena(self):
        NumberEdges = {
            0: {"a": True, "b": True, "c": True, "d": True, "e": False, "f": True, "g": True},
            1: {"a": False, "b": False, "c": True, "d": False, "e": False, "f": True, "g": False},
            2: {"a": False, "b": True, "c": True, "d": True, "e": True, "f": False, "g": True},
            3: {"a": False, "b": True, "c": True, "d": False, "e": True, "f": True, "g": True},
            4: {"a": True, "b": False, "c": True, "d": False, "e": True, "f": True, "g": False},
            5: {"a": True, "b": True, "c": False, "d": False, "e": True, "f": True, "g": True},
            6: {"a": True, "b": True, "c": False, "d": True, "e": True, "f": True, "g": True},
            7: {"a": False, "b": True, "c": True, "d": False, "e": False, "f": True, "g": False},
            8: {"a": True, "b": True, "c": True, "d": True, "e": True, "f": True, "g": True},
            9: {"a": True, "b": True, "c": True, "d": False, "e": True, "f": True, "g": False}
        }
        NumberPaths = {
            'a': [("turn_right", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 35)],
            'b': [("turn_right", None), ("move_forward", 35), ("turn_left", None), ("move_forward", 35)],
            'c': [("move_forward", 35), ("turn_right", None)],
            'd': [("turn_right", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 105), ("turn_left", None), ("move_forward", 70), ("turn_left", None), ("move_forward", 35), ("turn_right", None)],
            'e': [("move_forward", 35)],
            'f': [("move_forward", 35), ("turn_left", None)],
            'g': [("turn_left", None), ('move_forward', 35), ("turn_right", None), ("move_forward", 35)]
        }


        actions = []
        boxes_availability = [False, False, False, False, False]

        # First check for box availability
        self.maze_go(0)
        self.maze_go(0)
        if self.right_dist_sensor.get_distance < 40:  # This method might not be very accurate so we might need to change it
            boxes_availability[0] = True             # to turn left and right and check for distance
        self.maze_go(2)
        if self.left_dist_sensor.get_distance < 40:
            boxes_availability[1] = True
        self.maze_go(2)
        self.maze_go(2)
        self.maze_go(2)
        self.maze_go(3)
        self.maze_go(3)
        self.maze_go(3)
        if self.left_dist_sensor.get_distance < 40:
            boxes_availability[2] = True
        self.maze_go(1)
        if self.right_dist_sensor.get_distance < 40:
            boxes_availability[3] = True
        self.maze_go(1)
        if self.left_dist_sensor.get_distance < 40:
            boxes_availability[4] = True
        self.maze_go(1)
        self.maze_go(0)
        self.maze_go(0)
        
        # def identify_number():
        #     # Move 35cm forward
        #     self.move_forward_distance(80, 35)
        #     actions.append(('move_forward', 35))
        #     # Check for barrier
        #     front_dist = self.front_dist_sensor.get_distance()
        #     if front_dist < 20:
        #         # Turn left
        #         self.turn_left()
        #         actions.append(('turn_left', None))
        #         # Check for barrier
        #         front_dist = self.front_dist_sensor.get_distance()
        #         if front_dist < 20:
        #             # Reverse
        #             self.reverse()
        #             actions.append(('reverse', None))
        #             # Check for barrier
        #             front_dist = self.front_dist_sensor.get_distance()
        #             if front_dist < 20:
        #                 # Turn right
        #                 self.turn_right()
        #                 actions.append(('turn_right', None))
        #                 # Move 35cm forward
        #                 self.move_forward_distance(80, 35)
        #                 actions.append(('move_forward', 35))
        #                 # Turn left
        #                 self.turn_left()
        #                 actions.append(('turn_left', None))
        #                 # Move 70cm forward
        #                 self.move_forward_distance(80, 70)
        #                 actions.append(('move_forward', 70))
        #                 # Turn left
        #                 self.turn_left()
        #                 actions.append(('turn_left', None))
        #                 # Move 70cm forward
        #                 self.move_forward_distance(80, 70)
        #                 actions.append(('move_forward', 70))
        #                 # Turn left
        #                 self.turn_left()
        #                 actions.append(('turn_left', None))
        #                 # Move 35cm forward
        #                 self.move_forward_distance(80, 35)
        #                 actions.append(('move_forward', 35))
        #                 # Check for barrier
        #                 front_dist = self.front_dist_sensor.get_distance()
        #                 if front_dist < 20:
        #                     # Turn left
        #                     self.turn_left()
        #                     actions.append(('turn_left', None))
        #                     # Check for barrier
        #                     front_dist = self.front_dist_sensor.get_distance()
        #                     if front_dist < 20:
        #                         # Reverse
        #                         self.reverse()
        #                         actions.append(('reverse', None))
        #                         # Move 35cm forward
        #                         self.move_forward_distance(80, 35)
        #                         actions.append(('move_forward', 35))
        #                         # Turn left
        #                         self.turn_left()
        #                         actions.append(('turn_left', None))
        #                         # Move 70cm forward
        #                         self.move_forward_distance(80, 70)
        #                         actions.append(('move_forward', 70))
        #                         # Turn left
        #                         self.turn_left()
        #                         actions.append(('turn_left', None))
        #                         # Move 35cm forward
        #                         self.move_forward_distance(80, 35)
        #                         actions.append(('move_forward', 35))
        #                         # Turn left
        #                         self.turn_left()
        #                         actions.append(('turn_left', None))
        #                         # Check for barrier
        #                         front_dist = self.front_dist_sensor.get_distance()
        #                         if front_dist < 20:
        #                             return 8
        #                         else:
        #                             return 9
        #                     else:
        #                         return 4
        #                 else:
        #                     return 3
        #             else:
        #                 # Move 70cm forward
        #                 self.move_forward_distance(80, 70)
        #                 actions.append(('move_forward', 70))
        #                 # Turn left
        #                 self.turn_left()
        #                 actions.append(('turn_left', None))
        #                 # Move 70cm forward
        #                 self.move_forward_distance(80, 70)
        #                 actions.append(('move_forward', 70))
        #                 # Turn left
        #                 self.turn_left()
        #                 actions.append(('turn_left', None))
        #                 # Move 70cm forward
        #                 self.move_forward_distance(80, 70)
        #                 actions.append(('move_forward', 70))
        #                 # Turn left
        #                 self.turn_left()
        #                 actions.append(('turn_left', None))
        #                 # Move 35cm forward
        #                 self.move_forward_distance(80, 35)
        #                 actions.append(('move_forward', 35))
        #                 # Turn right
        #                 self.turn_right()
        #                 actions.append(('turn_right', None))
        #                 # Check for barrier
        #                 front_dist = self.front_dist_sensor.get_distance()
        #                 if front_dist < 20:
        #                     return 6
        #                 else:
        #                     return 5
        #         else:
        #             return 2
        #     else:
        #         # Move 35cm forward
        #         self.move_forward_distance(80, 35)
        #         actions.append(('move_forward', 35))
        #         # Turn right
        #         self.turn_right()
        #         actions.append(('turn_right', None))
        #         # Check for barrier
        #         front_dist = self.front_dist_sensor.get_distance()
        #         if front_dist < 20:
        #             return 0
        #         else:
        #             # Move 35cm forward
        #             self.move_forward_distance(80, 35)
        #             actions.append(('move_forward', 35))
        #             # Turn right
        #             self.turn_right()
        #             actions.append(('turn_right', None))
        #             # Check for barrier
        #             front_dist = self.front_dist_sensor.get_distance()
        #             if front_dist < 20:
        #                 return 7
        #             else:
        #                 return 1

        #     self.reverse()
        #     self.undo_actions(actions)
        #     self.reverse()

        # def build_number():
        #     prev_number = identify_number()
        #     prev_number_edges = NumberEdges[prev_number]
        #     next_number = 7
        #     next_number_edges = NumbersEdges[next_number]
        #     for i in range(ord('a'), ord('g')+1):
        #         if not(prev_number_edges[chr(i)]) and next_number_edges[chr(i)]:
        #             for action in BoxesPaths[boxes_availability.index(True)]:
        #                 self.do_action(action[0], action[1])
        #                 actions.append(action)
        #             boxes_availability[boxes_availability.index(True)] = False
        #             self.reverse()
        #             self.undo_actions(actions)
        #             self.reverse()
        #             for action in NumberPaths[chr(i)]:
        #                 self.do_action(action[0], action[1])
        #                 actions.append(action)
        #             self.reverse()
        #             self.undo_actions(actions)
        #             self.reverse()
        #         if prev_number_edges[chr(i)] and not(next_number_edges[chr(i)]):
        #             for action in NumberPaths[chr(i)]:
        #                 self.do_action(action[0], action[1])
        #                 actions.append(action)
        #             self.reverse()
        #             self.undo_actions(actions)
        #             self.reverse()
        #             for action in BoxesPaths[boxes_availability.index(False)]:
        #                 self.do_action(action[0], action[1])
        #                 actions.append(action)
        #             self.reverse()
        #             self.undo_actions(actions)
        #             self.reverse()