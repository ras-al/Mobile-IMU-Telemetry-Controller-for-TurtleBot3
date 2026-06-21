import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import math

class MobileImuController(Node):
    def __init__(self):
        super().__init__('mobile_imu_telop')

        #1. Setup publisher for turtlebot3 velocity
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)

        #2.setup udp socket
        self.udp_ip = "0.0.0.0" 
        self.udp_port = 1212
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))

        self.sock.settimeout(0.01)

        self.get_logger().info(f"Listening for UDP telemetry on {self.udp_port}...")

        #3. Create a timer to run the control loop at 20Hz(0.05 s)
        self.timer = self.create_timer(0.05, self.timer_callback)

        #tuning para
        self.k_linear = 0.5
        self.k_angular = 1.0

    def timer_callback(self):
        try:
            # 1. Drain the socket to get the freshest data packet
            latest_data = None
            while True:
                try:
                    latest_data, _ = self.sock.recvfrom(4096)
                except socket.timeout:
                    break
            
            if latest_data is None:
                return
            
            # 2. Decode and Parse
            raw_string = latest_data.decode("utf-8").strip()
            groups = raw_string.split("|")
            
            if len(groups) < 3:
                self.get_logger().warn(f"Incomplete packet received: {raw_string}")
                return

            acc = [float(v) for v in groups[0].split(",")]
            ax, ay, az = acc[0], acc[1], acc[2]

            # 3. Kinematics
            pitch = math.atan2(-ay, az)
            roll = math.atan2(ax, az)

            vel_msg = Twist()
            vel_msg.linear.x = pitch * self.k_linear
            vel_msg.angular.z = roll * self.k_angular

            # 4. Publish to ROS
            self.publisher_.publish(vel_msg)
            
            # 5. Log the output to terminal for debugging
            self.get_logger().info(f"Published -> Linear: {vel_msg.linear.x:.2f} | Angular: {vel_msg.angular.z:.2f}")

        except Exception as e:
            self.get_logger().error(f"Parsing Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    imu_controller = MobileImuController()

    try:
        rclpy.spin(imu_controller)
    except KeyboardInterrupt:
        pass
    finally:
        imu_controller.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main() 