import zerorpc
from franky import *
import math
from scipy.spatial.transform import Rotation
import numpy as np

class FrankaInterface:
    def __init__(self):
        self.robot = Robot("172.16.0.2")
        self.robot.relative_dynamics_factor = 0.05

    def get_ee_pose(self):
        cartesian_state = self.robot.current_cartesian_state
        robot_pose = cartesian_state.pose  # Contains end-effector pose and elbow position
        ee_pose = robot_pose.end_effector_pose
        position = ee_pose.translation.copy()  # 或 ee_pose.t
        orientation = ee_pose.quaternion  # 或 ee_pose.q

        rot_vec = Rotation.from_quat(orientation).as_rotvec()
        return np.concatenate([position, rot_vec]).tolist()
    
    def update_desired_ee_pose(self, pose):
        pose = np.asarray(pose)
        position = pose[:3]
        orientation = Rotation.from_rotvec(pose[3:]).as_quat()
        m_cp1 = CartesianMotion(Affine(position, orientation))
        self.robot.move(m_cp1)

# if __name__ == "__main__":
#     robot =  FrankaInterface() 
#     print(robot.get_joint_positions())

s = zerorpc.Server(FrankaInterface())
s.bind("tcp://0.0.0.0:4242")
s.run()