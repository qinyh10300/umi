import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
os.chdir(ROOT_DIR)

import time
import numpy as np
from scipy.spatial.transform import Rotation as R
from umi.real_world.franka_interpolation_controller import FrankaInterface
from umi.common.pose_util import pose_to_mat, mat_to_pose

TRANSLATION_MODES = ("x", "y", "z")
ROTATION_MODES = ("r", "p", "yy")
AVAILABLE_MODES = TRANSLATION_MODES + ROTATION_MODES

def askForCommand():
    strAskForCommand  = '\n可用指令\n\n'
    strAskForCommand += 'x/y/z: 微调x/y/z轴位置\n'
    strAskForCommand += 'r/p/yy: 微调r/p/y欧拉角\n'
    strAskForCommand += 'w: 正方向平移/旋转一个步长\n'
    strAskForCommand += 's: 向负方向平移/旋转一个步长\n'
    strAskForCommand += 'tstep: 设置平移的步长（单位m）\n'
    strAskForCommand += 'rstep: 设置微调转角的步长（单位度）\n'
    strAskForCommand += 'h: 显示此提示，也可用于刷新显示的机械臂状态\n'
    strAskForCommand += '直接回车可以复用上一次的指令\n'

    print(strAskForCommand)

if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    Franka = FrankaInterface(ip='183.173.65.137', port=4242)

    Kx_scale = 1.0
    Kxd_scale = 1.0
    Kx = np.array([750.0, 750.0, 750.0, 15.0, 15.0, 15.0]) * Kx_scale
    Kxd = np.array([37.0, 37.0, 37.0, 2.0, 2.0, 2.0]) * Kxd_scale

    # start franka cartesian impedance policy
    Franka.start_cartesian_impedance(
        Kx=Kx,
        Kxd=Kxd
    )

    current_mode: str = "x"

    translation_step: float = 0.02
    rotation_step: float = 2 # 单位°
    last_command: str = ""
    time_to_go: float = 0.5

    askForCommand()
    while True:
        # 获取当前机械臂状态
        pose_current_mat = pose_to_mat(Franka.get_raw_ee_pos())

        rpy: np.ndarray = R.from_matrix(pose_current_mat[:3,:3]).as_euler('xyz', degrees=True)
        xyz: np.ndarray = pose_current_mat[:3,3]

        # 打印当前状态并获取指令
        translation_mode: bool = current_mode in TRANSLATION_MODES
        current_step: float = translation_step if translation_mode else rotation_step
        mode_str = "当前模式：%s%s, 步长：%.2f%s" % (current_mode[0].upper(), "轴平移" if translation_mode else "角旋转",
                                                    current_step, "m" if translation_mode else "°")
        inp = input("%s, 当前xyz位移：%s, 当前rpy转角: [%.2f°, %.2f°, %.2f°], 输入指令:" % (mode_str, np.array2string(xyz), rpy[0], rpy[1], rpy[2])).lower()

        # 保存/调出历史指令
        if len(inp) == 0:
            inp = last_command
        else:
            last_command = inp

        # 解析指令
        if inp in AVAILABLE_MODES:
            current_mode = inp
            print("切换到{} (y为position，yy为欧拉角)".format(current_mode))
        elif inp == 'rstep':
            inp = input("输入rotation新步长(°):")
            try:
                rotation_step = float(inp)
            except ValueError:
                print("无效步长, 设置失败")
        elif inp == 'tstep':
            inp = input("输入translation新步长(m):")
            try:
                translation_step = float(inp)
            except ValueError:
                print("无效步长, 设置失败")
        elif inp == 'w' or inp == 's':
            sign: int = 1 if inp == 'w' else -1

            if translation_mode:
                xyz[TRANSLATION_MODES.index(current_mode)] += current_step * sign
            else:
                rpy[ROTATION_MODES.index(current_mode)] += current_step * sign

            # 计算目标姿态
            pose_current_mat[:3,:3] = R.from_euler('xyz', rpy, degrees=True).as_matrix()
            pose_current_mat[:3,3] = xyz

            # 移动机械臂
            Franka.update_desired_ee_pose(mat_to_pose(pose_current_mat))
        else:
            askForCommand()

        time.sleep(0.1)
