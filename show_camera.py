import cv2
import argparse

def capture_and_display_camera(camera_path='/dev/video0'):
    """
    读取指定路径摄像头的图像并实时显示
    按"q"键退出程序
    
    参数:
        camera_path: 摄像头设备路径，默认为'/dev/video0'
    """
    # 尝试打开摄像头
    try:
        # 对于USB摄像头，可以直接使用数字索引（0, 1, 2...）或完整路径
        cap = cv2.VideoCapture(camera_path)
        
        # 检查摄像头是否成功打开
        if not cap.isOpened():
            print(f"错误：无法打开摄像头 {camera_path}")
            return
        
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        # set fps
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        cap.set(cv2.CAP_PROP_FPS, 60)
        
        print(f"成功打开摄像头: {camera_path}")
        print("按 'q' 键退出")
        
        # 循环读取和显示帧
        while True:
            # 读取一帧
            ret, frame = cap.read()
            
            # 如果读取失败，退出循环
            if not ret:
                print("无法获取图像帧，退出...")
                break
            
            # 显示图像
            cv2.imshow('Camera Feed', frame)
            
            # 等待键盘输入，如果是'q'则退出
            # waitKey(1)表示等待1毫秒
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("用户按下'q'键，退出程序")
                break
                
    except Exception as e:
        print(f"发生错误: {e}")
    
    finally:
        # 释放资源
        if 'cap' in locals() and cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("已关闭摄像头和所有窗口")

if __name__ == "__main__":
    # 使用命令行参数允许用户指定摄像头路径
    parser = argparse.ArgumentParser(description='显示Ubuntu系统摄像头图像')
    parser.add_argument('--camera', type=str, default='/dev/video4',
                        help='摄像头设备路径 (默认: /dev/video0)')
    args = parser.parse_args()
    
    # 调用主函数
    capture_and_display_camera(args.camera)