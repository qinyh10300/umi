import numpy as np
import cv2
import json

def extract_rotation_translation(transform_matrix):
    R = transform_matrix[:3, :3]
    t = transform_matrix[:3, 3].reshape(3, 1)
    return R, t

def calibrate_hand_eye(ee_2_base_matrices, marker_2_cam_matrices):

    R1_list = [] 
    t1_list = [] 
    R2_list = []  
    t2_list = [] 
    
    for A, B in zip(ee_2_base_matrices, marker_2_cam_matrices):
        R1, t1 = extract_rotation_translation(A)
        R2, t2 = extract_rotation_translation(B)
        
        R1_list.append(R1) 
        t1_list.append(t1)
        R2_list.append(R2) 
        t2_list.append(t2)
    
    # 转换为OpenCV需要的格式
    R1_list = [R.astype(np.float64) for R in R1_list]
    t1_list = [t.astype(np.float64) for t in t1_list]
    R2_list = [R.astype(np.float64) for R in R2_list]
    t2_list = [t.astype(np.float64) for t in t2_list]
    
    # 使用OpenCV的calibrateHandEye函数
    R_quest_to_flange, t_quest_to_flange = cv2.calibrateHandEye(
        R1_list, t1_list,
        R2_list, t2_list,
        method=cv2.CALIB_HAND_EYE_TSAI  # 使用Tsai's 方法
    )
    
    # 构建4x4变换矩阵
    quest_to_flange = np.eye(4)
    quest_to_flange[:3, :3] = R_quest_to_flange
    quest_to_flange[:3, 3] = t_quest_to_flange.flatten()

    
    return quest_to_flange


if __name__ == "__main__":
    # ee_2_base_matrices = np.load('E:\\codehub\\ViTaMIn-B\\Data_collection\\data.npy')
    with open('E:\\codehub\\ViTaMIn-B\\Data_collection\\assets\\data\\record_cartesian_calibration(5).json', 'r') as f:
        ee_2_base_matrices = json.load(f)
    ee_2_base_matrices = [np.array(matrix) for matrix in ee_2_base_matrices.values()]

    marker_2_cam_matrices = np.load('E:\\codehub\\ViTaMIn-B\\Data_collection\\assets\\data\\cali_cam_ee_imgs\\cam_poses.npy')
    X = calibrate_hand_eye(ee_2_base_matrices, marker_2_cam_matrices)
    print("\nCamera to ee transformation matrix:")
    print(X)
    
    # 保存结果
    np.save('cam_2_ee.npy', X)
    print("\nResult saved to cam_2_ee.npy")