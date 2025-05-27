import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
os.chdir(ROOT_DIR)

import numpy as np
import zerorpc

class FrankaGripperInterface:
    def __init__(self, ip='183.173.66.202', port=4241):
        self.server = zerorpc.Client(heartbeat=20)
        self.server.connect(f"tcp://{ip}:{port}")

    def get_pos(self):
        state = self.server.get_pos()
        return state
    
    def set_pos(self, pos):
        self.server.set_pos(pos)

    def set_speed(self, speed):
        self.server.set_speed(speed)

    def open(self):
        self.server.open()

if __name__ == "__main__":
    robot = FrankaGripperInterface(ip='183.173.65.143', port=4241)
    print(robot.get_pos())

    robot.set_speed(speed=0.02)

    robot.set_pos(pos=0.0)

    # robot.move(pos=0.0)