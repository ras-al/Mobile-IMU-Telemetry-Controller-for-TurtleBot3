import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import socket
import math

class MobileImuController(Node):
    def __init__(self):
        super().__init__('mobile_imu_telop')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        
        self.udp_ip = "0.0.0.0" 
        self.udp_port = 1212
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.udp_ip, self.udp_port))
        self.sock.settimeout(0.01)

        self.timer = self.create_timer(0.05, self.timer_callback)

        self.k_linear = 0.5
        self.k_angular = 1.0

        # Filter Variables
        self.pitch_history = []
        self.roll_history = []
        self.window_size = 5

        # Calibration Variables
        self.is_calibrating = True
        self.calibration_samples = []
        self.pitch_offset = 0.0
        self.roll_offset = 0.0
        self.get_logger().info("Please hold the phone flat and still for 2 seconds...")

    def timer_callback(self):
        try:
            latest_data = None
            while True:
                try:
                    latest_data, _ = self.sock.recvfrom(4096)
                except socket.timeout:
                    break
            
            if latest_data is None: return
            
            raw_string = latest_data.decode("utf-8").strip()
            groups = raw_string.split("|")
            if len(groups) < 3: return

            acc = [float(v) for v in groups[0].split(",")]
            ax, ay, az = acc[0], acc[1], acc[2]

            # Raw Kinematics
            raw_pitch = math.atan2(-ay, az)
            raw_roll = math.atan2(ax, az)

            # Calibration Routine
            if self.is_calibrating:
                self.calibration_samples.append((raw_pitch, raw_roll))
                # 40 samples at 20Hz = 2 seconds of calibration
                if len(self.calibration_samples) >= 40:
                    self.pitch_offset = sum(p for p, r in self.calibration_samples) / 40
                    self.roll_offset = sum(r for p, r in self.calibration_samples) / 40
                    self.is_calibrating = False
                    self.get_logger().info(f"Calibration Complete! (Offsets - Pitch: {self.pitch_offset:.2f}, Roll: {self.roll_offset:.2f})")
                return

            # Apply Calibration Offsets
            calibrated_pitch = raw_pitch - self.pitch_offset
            calibrated_roll = raw_roll - self.roll_offset

            # SMA Filter (using calibrated values)
            self.pitch_history.append(calibrated_pitch)
            self.roll_history.append(calibrated_roll)

            if len(self.pitch_history) > self.window_size:
                self.pitch_history.pop(0)
                self.roll_history.pop(0)

            smooth_pitch = sum(self.pitch_history) / len(self.pitch_history)
            smooth_roll = sum(self.roll_history) / len(self.roll_history)

            # Deadzone
            if abs(smooth_pitch) < 0.1: smooth_pitch = 0.0
            if abs(smooth_roll) < 0.1: smooth_roll = 0.0

            vel_msg = Twist()
            vel_msg.linear.x = smooth_pitch * self.k_linear
            vel_msg.angular.z = smooth_roll * self.k_angular

            self.publisher_.publish(vel_msg)
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