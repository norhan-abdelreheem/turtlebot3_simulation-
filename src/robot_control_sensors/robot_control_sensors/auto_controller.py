import math
import time

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from geometry_msgs.msg import TwistStamped
from sensor_msgs.msg import LaserScan


class AutoController(Node):

    def __init__(self):
        super().__init__('auto_controller')

        self.safe_distance = 0.30
        self.linear_speed = 0.05
        self.scan_timeout = 2.0

        self.front_distance = None
        self.last_scan_time = None
        self.last_status = None
        self.obstacle_latched = False

        self.declare_parameter('enable_motion', False)

        self.publisher = self.create_publisher(
            TwistStamped,
            '/cmd_vel',
            10
        )

        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        self.create_timer(0.1, self.control_robot)

        self.get_logger().info('Auto Controller Started')

    def scan_callback(self, msg):

        front_ranges = []
        invalid = False

        for i, distance in enumerate(msg.ranges):

            angle = msg.angle_min + i * msg.angle_increment
            angle = math.degrees(angle)
            angle = (angle + 180) % 360 - 180

            if -30 <= angle <= 30:

                if distance == math.inf:
                    front_ranges.append(msg.range_max)

                elif (
                    math.isfinite(distance)
                    and msg.range_min <= distance <= msg.range_max
                ):
                    front_ranges.append(distance)

                else:
                    invalid = True

        self.last_scan_time = time.monotonic()

        if front_ranges and not invalid:
            self.front_distance = min(front_ranges)
        else:
            self.front_distance = None

    def control_robot(self):

        enabled = self.get_parameter(
            'enable_motion'
        ).value

        if not enabled:
            self.obstacle_latched = False
            self.stop_robot()
            self.report_status('Motion Disabled')
            return

        if (
            self.last_scan_time is None
            or time.monotonic() - self.last_scan_time
            > self.scan_timeout
        ):
            self.stop_robot()
            self.report_status('STOP: LiDAR data missing')
            return

        if self.front_distance is None:
            self.stop_robot()
            self.report_status('STOP: Invalid LiDAR data')
            return

        if self.front_distance <= self.safe_distance:
            self.obstacle_latched = True

        if self.obstacle_latched:
            self.stop_robot()
            self.report_status('STOP: Obstacle detected')

        else:
            self.send_velocity(self.linear_speed)
            self.report_status('MOVING FORWARD')

    def send_velocity(self, speed):

        msg = TwistStamped()

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'

        msg.twist.linear.x = float(speed)
        msg.twist.angular.z = 0.0

        self.publisher.publish(msg)

    def stop_robot(self):
        self.send_velocity(0.0)

    def report_status(self, status):

        if status != self.last_status:
            self.get_logger().info(status)
            self.last_status = status


def main(args=None):

    rclpy.init(args=args)
    node = AutoController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:

        if rclpy.ok():
            node.stop_robot()

        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
