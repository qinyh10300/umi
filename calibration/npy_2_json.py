import numpy as np
import json
import os

# 读取NPY文件
npy_file_path = 'calibration/cam_2_ee.npy'
array_data = np.load(npy_file_path)

# 将NumPy数组转换为Python列表
data_list = array_data.tolist()

# 如果想将多个数组保存在一个字典中
data_dict = {
    "cam_poses": data_list,
    # 可以添加更多数组
    # "other_data": other_array.tolist()
}

# 或者如果是多个矩阵，可以按索引存储
# data_dict = {str(i): matrix.tolist() for i, matrix in enumerate(array_data)}

# 指定JSON文件保存路径
json_file_path = 'calibration/cam_2_ee.json'

# 确保目录存在
os.makedirs(os.path.dirname(json_file_path), exist_ok=True)

# 保存为JSON文件
with open(json_file_path, 'w') as f:
    json.dump(data_dict, f, indent=4)

print(f"NPY数据已成功保存为JSON文件：{json_file_path}")