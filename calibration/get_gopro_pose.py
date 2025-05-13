import cv2
import numpy as np
import os

import sys
root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
# print(root_dir)
sys.path.append(root_dir)

import json
import glob
from calibration.cv_utils import parse_fisheye_intrinsics, convert_fisheye_intrinsics_resolution

def get_pose_from_image(image_path, camera_matrix, dist_coeffs, aruco_size, target_id_left, output_path=None):
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    parameters = cv2.aruco.DetectorParameters()
    detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
    
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Error: Could not read image {image_path}")
        return None
    
    corners, ids, _ = detector.detectMarkers(img)
    
    pose_matrix = None
    
    if ids is not None:
        target_idx = np.where(ids == target_id_left)[0]
        
        if len(target_idx) > 0:
            idx = target_idx[0]
            undistorted = cv2.fisheye.undistortPoints(corners[idx:idx+1][0], camera_matrix, dist_coeffs, P=camera_matrix)
            rvecs, tvecs, _ = cv2.aruco.estimatePoseSingleMarkers(undistorted, aruco_size, camera_matrix, np.zeros((1,5)))
            
            R, _ = cv2.Rodrigues(rvecs[0])
            
            pose_matrix = np.eye(4)
            pose_matrix[:3, :3] = R
            pose_matrix[:3, 3] = tvecs[0].flatten()
            
            if output_path:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                np.save(output_path, pose_matrix)
                print(f"Pose matrix saved to {output_path}")
                
            print(f"Pose matrix:\n{pose_matrix}")
    else:
        print(f"No ArUco markers with ID {target_id_left} detected in the image")
    
    return pose_matrix

def get_poses_from_images(image_paths, camera_matrix, dist_coeffs, aruco_size, target_id, output_dir, output_filename="all_poses.npy"):
    os.makedirs(output_dir, exist_ok=True)
    
    if isinstance(image_paths, str) and os.path.isdir(image_paths):
        image_paths = sorted(glob.glob(os.path.join(image_paths, "*.JPG")))
        print(f"Found {len(image_paths)} images in directory")
    
    poses = []
    
    for i, img_path in enumerate(image_paths):
        print(f"Processing image {i+1}/{len(image_paths)}: {img_path}")
        
        # Don't save individual pose files anymore
        pose = get_pose_from_image(
            image_path=img_path,
            camera_matrix=camera_matrix,
            dist_coeffs=dist_coeffs,
            aruco_size=aruco_size,
            target_id_left=target_id,
            output_path=None  # Don't save individual files
        )
        
        if pose is not None:
            poses.append(pose)
    
    # Save all poses as a single array
    if poses:
        poses_array = np.array(poses)
        all_poses_path = os.path.join(output_dir, output_filename)
        np.save(all_poses_path, poses_array)
        print(f"All poses saved to {all_poses_path}")
    
    return poses

if __name__ == "__main__":
    intr_json = "assets/gopro_intrinsics_2_7k.json"
    raw_fisheye_intr = parse_fisheye_intrinsics(json.load(open(intr_json, 'r')))
    res = (5568, 4176)
    fisheye_intr = convert_fisheye_intrinsics_resolution(
        opencv_intr_dict=raw_fisheye_intr, target_resolution=res)
    K = fisheye_intr['K']
    D = fisheye_intr['D']
    aruco_size = 0.2 
    target_id = 35
    image_dir = "E:\\codehub\\ViTaMIn-B\\Data_collection\\assets\\data\\cali_cam_ee_imgs"
    output_dir = "E:\\codehub\ViTaMIn-B\\Data_collection\\assets\\data\\cali_cam_ee_imgs"
    output_filename = "cam_poses.npy"  # Specify the output filename
    
    poses = get_poses_from_images(
        image_paths=image_dir,
        camera_matrix=K,
        dist_coeffs=D,
        aruco_size=aruco_size,
        target_id=target_id,
        output_dir=output_dir,
        output_filename=output_filename  # Pass the filename
    )
    