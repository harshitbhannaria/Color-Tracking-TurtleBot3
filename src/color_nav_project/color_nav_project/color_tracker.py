import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, LaserScan
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np

class ColorTracker(Node):
    def __init__(self):
        super().__init__('color_tracker')
        
        self.img_sub = self.create_subscription(Image, '/camera/image_raw', self.image_callback, 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.bridge = CvBridge()
        self.min_dist = 10.0
        
        # PID Constants
        self.kp = 0.002
        self.ki = 0.0001  
        self.kd = 0.001
        
        # Error History
        self.prev_error = 0.0
        self.integral = 0.0
        self.error_threshold = 10.0 # Deadzone
        
        self.get_logger().info("--- Anti-Accumulation PID Node Started ---")

    def scan_callback(self, msg):
        front_ranges = [r for r in msg.ranges[0:20] + msg.ranges[-20:] if np.isfinite(r)]
        self.min_dist = min(front_ranges) if front_ranges else 10.0

    def image_callback(self, msg):
        try:
            frame = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            
            # Focused Green Mask
            mask = cv2.inRange(hsv, np.array([35, 90, 20]), np.array([85, 255, 255]))
            
            cv2.imshow("PID Mask View", mask)
            cv2.waitKey(1)
            
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            twist = Twist()

            if contours:
                largest = max(contours, key=cv2.contourArea)
                M = cv2.moments(largest)
                
                if M['m00'] > 500:
                    cx = int(M['m10'] / M['m00'])
                    current_error = float(cx - (frame.shape[1] / 2))

                    # 1. INTEGRAL (with clamping to prevent accumulation)
                    if abs(current_error) > self.error_threshold:
                        self.integral += current_error
                        # Anti-Windup: Limit how much the integral can "push"
                        self.integral = max(min(self.integral, 50.0), -50.0)
                    else:
                        self.integral = 0.0 # Clear error when we are "close enough"

                    # 2. DERIVATIVE
                    derivative = current_error - self.prev_error

                    # 3. PID FORMULA
                    angular_vel = (self.kp * current_error) + (self.ki * self.integral) + (self.kd * derivative)
                    
                    # Clamp the output to prevent violent spinning
                    twist.angular.z = -max(min(angular_vel, 0.8), -0.8)
                    
                    self.prev_error = current_error

                    # 4. LINEAR MOVEMENT
                    if abs(current_error) < 40:
                        if self.min_dist > 0.6:
                            # Smooth approach speed
                            twist.linear.x = min(0.15, (self.min_dist - 0.5) * 0.4)
                        else:
                            twist.linear.x = 0.0
                            self.get_logger().info('Target reached accurately.')
                    else:
                        twist.linear.x = 0.02 # Crawl while turning
                else:
                    self.search_mode(twist)
            else:
                self.search_mode(twist)

            self.cmd_pub.publish(twist)

        except Exception as e:
            self.get_logger().error(f"Error: {e}")

    def search_mode(self, twist):
        self.integral = 0.0 # Reset accumulation when target lost
        self.prev_error = 0.0
        twist.linear.x = 0.0
        twist.angular.z = 0.4

def main(args=None):
    rclpy.init(args=args)
    node = ColorTracker()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
