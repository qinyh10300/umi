import zerorpc
import scipy.spatial.transform as st
import numpy as np

import franky


class FrankaGripperInterface:
    def __init__(self):
        self.gripper = franky.Gripper("172.16.0.2")
        self.speed = 0.02  # [m/s]
        self.force = 20.0  # [N]
        
    def get_pos(self):
        # print(f"111   {self.gripper.width}")
        return self.gripper.width
    
    def set_pos(self, pose):
        # Move the fingers to a specific width (5cm)
        return self.gripper.move(pose, self.speed)
    
    def set_speed(self, speed=0.02):
        self.speed = speed

    def get_speed(self):
        return self.speed

    def grasp(self):
        # Grasp an object of unknown width
        return self.gripper.grasp(0.0, self.speed, self.force, epsilon_outer=1.0)

    def open(self):
        # Release the object
        self.gripper.open(self.speed)
    

# if __name__ == "__main__":
#     robot =  FrankaGripperInterface() 
#     print(robot.get_state())

s = zerorpc.Server(FrankaGripperInterface())
s.bind("tcp://0.0.0.0:4241")
s.run()

# from polymetis import GripperInterface

# gripper = GripperInterface(
#     ip_address="localhost",
# )

# # example usages
# gripper_state = gripper.get_state()
# gripper.goto(width=0.01, speed=0.05, force=0.1)
# # gripper.grasp(speed=0.05, force=0.1)