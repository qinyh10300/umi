from franky import *
import math
from scipy.spatial.transform import Rotation

robot = Robot("172.16.0.2")

# Get the current state as `franky.RobotState`. See the documentation for a list of fields.
state = robot.state

# Reduce velocity and acceleration of the robot
robot.relative_dynamics_factor = 0.05

# Get the robot's cartesian state
cartesian_state = robot.current_cartesian_state
robot_pose = cartesian_state.pose  # Contains end-effector pose and elbow position
ee_pose = robot_pose.end_effector_pose
# 访问位置向量
position = ee_pose.translation.copy()  # 或 ee_pose.t

# 访问旋转四元数
orientation = ee_pose.quaternion  # 或 ee_pose.q

print(position)
position[2] += 0.01
print(position)

quat = Rotation.from_euler("xyz", [0, 0, math.pi / 2]).as_quat()
print(quat, orientation, type(quat), type(orientation))

m_cp1 = CartesianMotion(Affine(position, orientation))

robot.move(m_cp1)
# print(ee_pose)
# print(position)
# print(orientation)

# Stop the robot in cartesian position control mode.
# m_cp6 = CartesianStopMotion()