import numpy as np
import json

def compute_hand_eye_error(ee_poses, cam_poses, hand_eye_matrix):
    """
    计算手眼标定误差
    :param ee_poses: 机械臂 EE 相对于 Base 的位姿列表 (4x4 矩阵)
    :param cam_poses: 相机相对于 ArUco 的位姿列表 (4x4 矩阵)
    :param hand_eye_matrix: 手眼矩阵 (4x4 矩阵)
    :return: 平均旋转误差 (degrees), 平均平移误差 (meters)
    """
    rotation_errors = []
    translation_errors = []

    for H_ee_base, H_marker_cam in zip(ee_poses, cam_poses):
        # 计算误差矩阵
        H_error = np.dot(np.dot(H_ee_base, hand_eye_matrix), H_marker_cam)

        # 提取旋转误差
        R_error = H_error[:3, :3]
        angle_error = np.arccos((np.trace(R_error) - 1) / 2)  # 旋转误差（弧度）
        rotation_errors.append(np.degrees(angle_error))  # 转换为角度

        # 提取平移误差
        t_error = H_error[:3, 3]
        print(t_error)
        translation_errors.append(np.linalg.norm(t_error))  # 欧几里得距离

    # 计算平均误差
    avg_rotation_error = np.mean(rotation_errors)
    avg_translation_error = np.mean(translation_errors)

    return avg_rotation_error, avg_translation_error

def load_poses_from_json(json_path):
    """从 JSON 文件加载位姿矩阵"""
    with open(json_path, "r") as f:
        data = json.load(f)
    poses = []
    for key in sorted(data.keys(), key=lambda x: int(x)):  # 按编号排序
        pose = np.array(data[key])
        poses.append(pose)
    return poses

# flange_2_base_matrices = np.load('E:\\codehub\\ViTaMIn-B\\Data_collection\\data.npy')
with open('E:\\codehub\\ViTaMIn-B\\Data_collection\\assets\\data\\record_cartesian_calibration(5).json', 'r') as f:
    ee_2_base_matrices = json.load(f)
    flange_2_base_matrices = [np.array(matrix) for matrix in ee_2_base_matrices.values()]
marker_2_cam_matrices = np.load('E:\\codehub\\ViTaMIn-B\\Data_collection\\assets\\data\\cali_cam_ee_imgs\\cam_poses.npy')
hand_eye_matrix = np.load('E:\\codehub\\ViTaMIn-B\\Data_collection\\cam_2_ee.npy')

avg_rotation_error, avg_translation_error = compute_hand_eye_error(flange_2_base_matrices, marker_2_cam_matrices, hand_eye_matrix)