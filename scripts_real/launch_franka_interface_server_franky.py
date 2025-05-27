from franky import *

robot = Robot("172.16.0.2")

# Get the current state as `franky.RobotState`. See the documentation for a list of fields.
state = robot.state
print(state)

# # Get the robot's cartesian state
# cartesian_state = robot.current_cartesian_state
# robot_pose = cartesian_state.pose  # Contains end-effector pose and elbow position
# ee_pose = robot_pose.end_effector_pose
# elbow_pos = robot_pose.elbow_state
# robot_velocity = cartesian_state.velocity  # Contains end-effector twist and elbow velocity
# ee_twist = robot_velocity.end_effector_twist
# elbow_vel = robot_velocity.elbow_velocity

# # Get the robot's joint state
# joint_state = robot.current_joint_state
# joint_pos = joint_state.position
# joint_vel = joint_state.velocity

# # Use the robot model to compute kinematics
# q = [-0.3, 0.1, 0.3, -1.4, 0.1, 1.8, 0.7]
# f_t_ee = Affine()
# ee_t_k = Affine()
# ee_pose_kin = robot.model.pose(Frame.EndEffector, q, f_t_ee, ee_t_k)

# # Get the jacobian of the current robot state
# jacobian = robot.model.body_jacobian(Frame.EndEffector, state)

# # Alternatively, just get the URDF as string and do the kinematics computation yourself (only for libfranka >= 0.15.0)
# urdf_model = robot.model_urdf

# import math
# from scipy.spatial.transform import Rotation
# from franky import *

# # Move to the given target pose
# quat = Rotation.from_euler("xyz", [0, 0, math.pi / 2]).as_quat()
# m_cp1 = CartesianMotion(Affine([0.4, -0.2, 0.3], quat))

# # With target elbow angle (otherwise, the Franka firmware will choose by itself)
# m_cp2 = CartesianMotion(RobotPose(Affine([0.4, -0.2, 0.3], quat), elbow_state=ElbowState(0.3)))

# # A linear motion in cartesian space relative to the initial position
# # (Note that this motion is relative both in position and orientation. Hence, when the robot's end-effector is oriented
# # differently, it will move in a different direction)
# m_cp3 = CartesianMotion(Affine([0.2, 0.0, 0.0]), ReferenceType.Relative)

# # Generalization of CartesianMotion that allows for multiple waypoints
# m_cp4 = CartesianWaypointMotion([
#     CartesianWaypoint(RobotPose(Affine([0.4, -0.2, 0.3], quat), elbow_state=ElbowState(0.3))),
#     # The following waypoint is relative to the prior one and 50% slower
#     CartesianWaypoint(Affine([0.2, 0.0, 0.0]), ReferenceType.Relative, RelativeDynamicsFactor(0.5, 1.0, 1.0))
# ])

# # Cartesian waypoints also permit to specify target velocities
# m_cp5 = CartesianWaypointMotion([
#     CartesianWaypoint(Affine([0.5, -0.2, 0.3], quat)),
#     CartesianWaypoint(
#         CartesianState(
#             pose=Affine([0.4, -0.1, 0.3], quat),
#             velocity=Twist([-0.01, 0.01, 0.0]))),
#     CartesianWaypoint(Affine([0.3, 0.0, 0.3], quat))
# ])

# # Stop the robot in cartesian position control mode.
# m_cp6 = CartesianStopMotion()