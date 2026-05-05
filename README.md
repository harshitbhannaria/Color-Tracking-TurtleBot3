# TurtleBot3 PID Color Tracking (ROS 2 Jazzy)

This project implements an autonomous color-tracking robot using **ROS 2 Jazzy**, **Gazebo Harmonic**, and **OpenCV**. The robot uses a PID controller to track a green sphere and LiDAR to maintain a safe stopping distance.

##  Features
- **Centroid Tracking**: Uses Image Moments (85196cx = M_{10} / M_{00}85196) to find the target.
- **PID Control**: Smooth navigation with anti-windup logic to prevent oscillations.
- **Gazebo Integration**: Custom SDF world with a high-contrast green sphere.

##  Usage
1. Launch the world: `gz sim -r green_sphere_world.sdf`
2. Start the bridge: `ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist /camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image`
3. Run the tracker: `ros2 run color_nav_project tracker`
