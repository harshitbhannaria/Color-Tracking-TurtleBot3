# TurtleBot3 PID Color Tracking (ROS 2 Jazzy)
# Autonomous Color Tracking with TurtleBot3 (ROS 2 Jazzy)

This project demonstrates a closed-loop control system where a TurtleBot3 Waffle detects, tracks, and approaches a green sphere in a simulated environment. It utilizes **OpenCV** for vision processing and a **PID Controller** for precise navigation.

## 🚀 Features
* **PID Control System:** Implemented Proportional-Derivative logic with Integral Anti-Windup to eliminate oscillations.
* **Computer Vision:** Real-time HSV thresholding and Centroid calculation using Image Moments.
* **Sensor Fusion:** Combines Camera data for steering and LiDAR data for precision braking.
* **Custom Environment:** A hand-coded `.sdf` world file optimized for high-contrast color detection.

---

## 🛠 Setup & Installation

### 1. Prerequisites
* **OS:** Ubuntu 24.04 (Noble)
* **Middleware:** ROS 2 Jazzy Jalisco
* **Simulator:** Gazebo Harmonic
* **Dependencies:** `ros-jazzy-ros-gz`, `python3-opencv`, `cv_bridge`

### 2. Workspace Setup
```bash
# Create and navigate to your workspace
mkdir -p ~/turtlebot3_ws/src
cd ~/turtlebot3_ws/src

# Clone this repository
git clone [https://github.com/YOUR_USERNAME/Color-Tracking-TurtleBot3.git](https://github.com/YOUR_USERNAME/Color-Tracking-TurtleBot3.git)

# Build the package
cd ~/turtlebot3_ws
colcon build --packages-select color_nav_project
source install/setup.bash
```


This project implements an autonomous color-tracking robot using **ROS 2 Jazzy**, **Gazebo Classic(fortress)** , and **OpenCV**. The robot uses a PID controller to track a green sphere and LiDAR to maintain a safe stopping distance.

##  Features
- **Centroid Tracking**: Uses Image Moments  to find the target.
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
Validate the **PID controller** without environmental interference.
Fine-tune the **HSV thresholding** values for the camera sensor.
Verify the **LiDAR-based braking system** against a known geometric shape.
