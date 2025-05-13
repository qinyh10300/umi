import zerorpc
import franky

class FrankaGripperInterface:
    def __init__(self):
        self.gripper = franky.Gripper("172.16.0.2")
        self.speed = 0.02  # [m/s]
        
    def get_state(self):  # [m]
        return self.gripper.width
    
    def set_pos(self, pos):  # [m]
        return self.gripper.move(pos, self.speed)
    
    def set_speed(self, speed):  # [m/s]
        self.speed = speed

# if __name__ == "__main__":
#     robot =  FrankaGripperInterface() 
#     print(robot.get_state())

s = zerorpc.Server(FrankaGripperInterface())
s.bind("tcp://0.0.0.0:4241")
s.run()