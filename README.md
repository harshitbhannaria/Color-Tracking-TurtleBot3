# TurtleBot3 PID Color Tracking (ROS 2 Jazzy)

This project implements an autonomous color-tracking robot using **ROS 2 Jazzy**, **Gazebo Harmonic**, and **OpenCV**. The robot uses a PID controller to track a green sphere and LiDAR to maintain a safe stopping distance.

##  Features
- **Centroid Tracking**: Uses Image Moments (85196cx = M_{10} / M_{00}85196) to find the target.
- **PID Control**: Smooth navigation with anti-windup logic to prevent oscillations.
- **Gazebo Integration**: Custom SDF world with a high-contrast green sphere.

##  Usage
1. Launch the world:
   `gz sim -r green_sphere_world.sdf`
3. Start the bridge:
   `ros2 run ros_gz_bridge parameter_bridge /cmd_vel@geometry_msgs/msg/Twist@gz.msgs.Twist /camera/image_raw@sensor_msgs/msg/Image[gz.msgs.Image`
4. Run the tracker:
   `ros2 run color_nav_project tracker`
   
## Environment Design: Custom Gazebo World
To test the tracking algorithm, I developed a custom Gazebo world (`green_sphere_world.sdf`) specifically designed for high-contrast computer vision tasks.

### The SDF Concept
The core idea was to create a "controlled experiment" environment. The SDF includes:
* **High-Emissivity Target:** A sphere with a specific green material script (`R: 0, G: 1, B: 0`) to ensure the OpenCV HSV mask can isolate it easily.
* **Ground Plane Calibration:** A standard gray plane to minimize background noise during the color filtering process.
* **Dynamic Physics:** The sphere is defined as a static model to ensure the robot doesn't physically "push" its target away, allowing for a precise approach and stop.

### Why not a standard world?
Standard Gazebo worlds often contain many colors and complex lighting that can interfere with basic color tracking. By creating a custom SDF, I was able to:
1. Validate the **PID controller** without environmental interference.
2. Fine-tune the **HSV thresholding** values for the camera sensor.
3. Verify the **LiDAR-based braking system** against a known geometric shape.
