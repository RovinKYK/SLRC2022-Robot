from turtle import color
from components import *

class Robot:
    def __init__(self):
        self.left_motor = RealMotor(25,23,22) #22,16,15
        self.right_motor = RealMotor(9,27,17) #21,13,11

        self.compass = Compass() #2,3 -> 3,5
        self.colour_sensor = ColourSensor(18,13,0,5,6) #12,33,27,29,31
        #self.encoder = Encoder(4) #7
        #self.push_button = PushButton() #

        self.front_middle_dist_sensor = DistanceSensor(20,12) #38,32
        self.front_left_dist_sensor = DistanceSensor(21,1) #40,28
        self.front_right_dist_sensor = DistanceSensor(26,7) #37,26
        self.side_left_dist_sensor = DistanceSensor(16,8) #36,24
        self.side_right_dist_sensor = DistanceSensor(19,11) #35,23

        self.middle_IR = IRSensor(15) #10
        self.inner_left_IR = IRSensor(14) #8
        self.inner_right_IR = IRSensor(4) #7
        self.outer_left_IR = IRSensor(24) #18
        self.outer_right_IR = IRSensor(10) #19

        #self.servo_motor
        self.curr_dir=0 # 0=north, 1=east, 2=south, 3=west   This will be useful for the grid areas
        self.visited=[20]
        self.speed=20

    def move_forward(self, speed):
        self.left_motor.move_forward(speed)
        self.right_motor.move_forward(speed)

    def move_backward(self, speed):
        self.left_motor.move_backward(speed)
        self.right_motor.move_backward(speed)

    def move_distance(self, distance, speed):
        self.left_motor.move_forward(speed)
        self.right_motor.move_forward(speed)

    def turn_left(self,speed=21,sleep_time=1): # 90 degree turn
        self.left_motor.move_backward(speed)
        self.right_motor.move_forward(speed)
        time.sleep(sleep_time)
        self.left_motor.stop()
        self.right_motor.stop()

    def turn_right(self,speed=21,sleep_time=1): # 90 degree turn
        self.left_motor.move_forward(speed)
        self.right_motor.move_backward(speed)
        time.sleep(sleep_time)
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
    def initial_line_follow(self,speed=25):
        t=time.time()
        while True:
            # read sensor values
            inner_left = self.inner_left_IR.detects_white()
            inner_right =self.inner_right_IR.detects_white()
            outer_left = self.outer_left_IR.detects_white()
            outer_right = self.outer_right_IR.detects_white()
            if time.time()-t>2:
                if outer_left or outer_right:
                    return
            if inner_left and not inner_right:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            if not inner_left and inner_right:
                self.left_motor.move_forward(speed)
                self.right_motor.move_backward(speed)
            else:
                self.move_forward(speed)
    def line_follow(self, speed=25):
        paths=[]
        time=time.time()
        while True:
            # read sensor values
            inner_left = self.inner_left_IR.detects_white()
            inner_right =self.inner_right_IR.detects_white()
            outer_left = self.outer_left_IR.detects_white()
            outer_right = self.outer_right_IR.detects_white()
            middle = not self.middle_IR.detects_white()

            # adjust motors based on sensor values
            # left 1
            # right 2
            # left and right 3
            # right and left 4
            # right and left and top 5
            # left and right and top 6
            # dead end 7
            if time.time()-time>1.5:
                if outer_left:
                    t = time.time()
                    is_outer_right=False
                    while True:
                        outer_left = self.outer_left_IR.detects_white()
                        outer_right = self.outer_right_IR.detects_white()
                        if outer_right:
                            is_outer_right=True
                        if not outer_right or time.time()-t>0.1:
                            colour="none"
                            self.stop()
                            while colour=="none":
                                colour=self.colour_sensor.detects_colour()
                                colour=self.colour_sensor.detects_colour()
                                colour=self.colour_sensor.detects_colour()
                                print(colour)
                            if colour=="red":
                                return 15
                            if colour=="green" or colour=="blue":
                                return paths
                            paths.append((self.curr_dir-1)%4)
                            if is_outer_right:
                                paths.append((self.curr_dir+1)%4)   
                            if colour=="white":
                                paths.append(self.curr_dir)
                            return paths 
                        self.move_forward(speed)
                if outer_right:
                    t = time.time()
                    is_outer_left=False
                    while True:
                        outer_left = self.outer_left_IR.detects_white()
                        outer_right = self.outer_right_IR.detects_white()
                        if outer_left:
                            is_outer_left=True
                        if not outer_right or time.time()-t>0.1:
                            colour="none"
                            self.stop()
                            while colour=="none":
                                colour=self.colour_sensor.detects_colour()
                                colour=self.colour_sensor.detects_colour()
                                colour=self.colour_sensor.detects_colour()
                                print(colour)
                            if colour=="red":
                                return 15
                            if colour=="green" or colour=="blue":
                                return paths
                            paths.append((self.curr_dir+1)%4)
                            if is_outer_left:
                                paths.append((self.curr_dir-1)%4)   
                            if colour=="white":
                                paths.append(self.curr_dir)
                            return paths 
                        self.move_forward(speed)
            if not (middle or inner_left or inner_right):
                self.stop()
                return paths
            if inner_left and not inner_right:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            if not inner_left and inner_right:
                self.left_motor.move_forward(speed)
                self.right_motor.move_backward(speed)
            else:
                self.move_forward(speed)
    def get_initial_paths(self,speed=25):
        paths=[]
        t=time.time()
        while True:
            outer_left=self.outer_left_IR.detects_white()
            outer_right=self.outer_right_IR.detects_white()
            if outer_left and not outer_right:
                self.left_motor.move_backward(speed)
                self.right_motor.move_forward(speed)
            elif not outer_left and outer_right:
                self.left_motor.move_forward(speed)
                self.right_motor.move_backward(speed)
            elif outer_left and outer_right :
                self.move_forward(speed)
            else:
                t=time.time()-t
                colour="none"
                self.stop()
                while colour=="none":
                    colour=self.colour_sensor.detects_colour()
                    colour=self.colour_sensor.detects_colour()
                    colour=self.colour_sensor.detects_colour()
                if colour=="white":
                    return
                else:
                    self.move_backward(speed)
                    time.sleep(t/3)
                    self.stop()
                    self.turn_left()
                    self.move_forward(speed)
                    time.sleep(t/3)
                    self.stop()
                    colour="none"
                    while colour=="none":
                        colour=self.colour_sensor.detects_colour()
                        colour=self.colour_sensor.detects_colour()
                        colour=self.colour_sensor.detects_colour()
                    if colour=="white":
                        return
                    else:
                        self.turn_right()
                        self.turn_right()
                        self.move_forward(speed)
                        time.sleep(t/3)
                        self.stop()
                        return 
        
    def arrow_follow(self, speed=25):
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
        self.line_follow(self.speed)
        # Move till the robot is in middle of the junction. calibrate exact values later
        self.curr_dir=direction
        # return (self.encoder.get_distance_moved//35)      # returns the number of junctions travelled

    def is_visited(self,current):      # this step won't be nessesary if there are no cycles in the maze
        destination=current+(-4 if self.curr_dir==0 else 1 if self.curr_dir==1 else 4 if self.curr_dir==2 else -1)
        if destination in self.visited:
            return True
        return False
        
    def turn_left_while_checking(self,speed=21):
        t = time.time()
        self.right_motor.move_backward(speed)
        self.left_motor.move_forward(speed)
        while time.time()-t<1:
            if self.outer_left_IR.detects_white():
                self.stop()
                return True
        self.stop()
        return False
    def turn_right_while_checking(self,speed=21):
        t = time.time()
        self.left_motor.move_backward(speed)
        self.right_motor.move_forward(speed)
        while time.time()-t<1:
            if self.outer_right_IR.detects_white():
                self.stop()
                return True
        self.stop()
        return False
    

    def run_line_maze_arena(self):
        # assuming that we start on middle of blue box facing west
        directions=['north','east','south','west']
        self.curr_dir=3
        pathToLast=[]       #path to the last turning point in reverse
        turningPoints=[]    #this is a stack of turning points
        current=20
        last_status=0
        while True:
            paths=self.line_follow(self.speed)
            print(paths)
            if paths==15:
                return
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
                self.visited.append(current)
        
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