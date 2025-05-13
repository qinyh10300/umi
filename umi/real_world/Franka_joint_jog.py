import sys
import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(ROOT_DIR)
os.chdir(ROOT_DIR)

import time
import math
import numpy as np
from typing import List
from scipy.spatial.transform import Rotation as R
from umi.real_world.franka_interpolation_controller import FrankaInterface


def askForCommand():
    strAskForCommand  = '\n可用指令\n\n'
    strAskForCommand += '(1-7): 切换至指定的joint\n'
    strAskForCommand += 'j: 调节运动步长\n'
    strAskForCommand += 'w: 当前joint向正方向旋转一个步长\n'
    strAskForCommand += 's: 当前joint向负方向旋转一个步长\n'
    strAskForCommand += 'g: 获取gripper2base矩阵\n'
    strAskForCommand += '直接回车可以复用上一次的指令\n'

    print(strAskForCommand)

if __name__ == "__main__":
    np.set_printoptions(precision=4, suppress=True)
    Franka = FrankaInterface(ip='183.173.65.137', port=4242)

    jog_step: float = 3 # in degree
    ctrl_joint: int = 1
    last_command: str = "1"
    time_to_go: float = 0.5

    askForCommand()
    while True:
        inp = input("当前joint:%d, 步长:%.1f°, 当前joint pos:%s, 输入指令:" % (ctrl_joint, jog_step, Franka.get_joint_positions()))
        if len(inp) == 0:
            inp = last_command
        else:
            last_command = inp

        try:
            joint_num = int(inp)
            if joint_num < 1 or joint_num > 7:
                raise ValueError()
            ctrl_joint = joint_num
            print("切换到joint %d" % ctrl_joint)
            continue
        except ValueError:
            pass

        if inp == 'j':
            inp = input("输入新步长(°):")
            try:
                jog_step = float(inp)
            except ValueError:
                print("无效步长, 设置失败")
        elif inp == 'w' or inp == 's':
            sign: int = 1 if inp == 'w' else -1
            curr_pose: List[float] = list(Franka.get_joint_positions())

            raw_pose = curr_pose[ctrl_joint-1]
            curr_pose[ctrl_joint-1] += math.radians(jog_step) * sign
            Franka.move_to_joint_positions(np.array(curr_pose), time_to_go)
            print("Joint %d pos %.4f -> %.4f," % (ctrl_joint, raw_pose, curr_pose[ctrl_joint-1]), "Sending:", np.asanyarray(curr_pose))
        else:
            askForCommand()

        time.sleep(0.1)
