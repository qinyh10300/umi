import franky

gripper = franky.Gripper("172.16.0.2")

speed = 0.02  # [m/s]
force = 20.0  # [N]

# Move the fingers to a specific width (5cm)
success = gripper.move(0.05, speed)

# Grasp an object of unknown width
success &= gripper.grasp(0.0, speed, force, epsilon_outer=1.0)

# Get the width of the grasped object
width = gripper.width

# Release the object
gripper.open(speed)

# There are also asynchronous versions of the methods
success_future = gripper.move_async(0.05, speed)

# Wait for 1s
if success_future.wait(1):
    print(f"Success: {success_future.get()}")
else:
    gripper.stop()
    success_future.wait()
    print("Gripper motion timed out.")