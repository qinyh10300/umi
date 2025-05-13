import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
os.chdir(ROOT_DIR)

import numpy as np
import zerorpc

class FrankaGripperInterface:
    def __init__(self, ip='183.173.65.137', port=4241):
        self.server = zerorpc.Client(heartbeat=20)
        self.server.connect(f"tcp://{ip}:{port}")

    def get_state(self):
        state = self.server.get_state()
        return state
    
    def set_pos(self, pos):
        self.server.set_pos(pos=pos)

    def set_speed(self, speed):
        self.server.set_speed(speed=speed)

if __name__ == "__main__":
    robot = FrankaGripperInterface(ip='183.173.67.70', port=4241)
    print(robot.get_state())

    robot.set_speed(speed=0.2)

    robot.set_pos(pos=0.0)