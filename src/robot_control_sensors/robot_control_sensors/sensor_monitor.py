import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data

from sensor_msgs.msg import LaserScan, Imu
from nav_msgs.msg import Odometry


class SensorMonitor(Node):

    def __init__(self):
        super().__init__('sensor_monitor')

        self.scan = None
        self.odom = None
        self.imu = None

        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            qos_profile_sensor_data
        )

        self.create_subscription(
            Imu,
            '/imu',
            self.imu_callback,
            qos_profile_sensor_data
        )

        self.create_timer(2.0, self.display_data)

        self.get_logger().info('Sensor Monitor Started')

    def scan_callback(self, msg):
        self.scan = msg

    def odom_callback(self, msg):
        self.odom = msg

    def imu_callback(self, msg):
        self.imu = msg

    def display_data(self):

        self.get_logger().info('----- SENSOR DATA -----')

        if self.scan is not None:

            valid_ranges = [
                distance for distance in self.scan.ranges
                if math.isfinite(distance)
                and self.scan.range_min <= distance
                <= self.scan.range_max
            ]

            if valid_ranges:
                nearest = min(valid_ranges)

                self.get_logger().info(
                    f'LiDAR: Nearest obstacle = {nearest:.2f} m'
                )
            else:
                self.get_logger().info(
                    'LiDAR: No valid distance readings'
                )
        else:
            self.get_logger().warn('Waiting for LiDAR data')

        if self.odom is not None:

            position = self.odom.pose.pose.position
            velocity = self.odom.twist.twist

            self.get_logger().info(
                f'Position: X={position.x:.2f}, '
                f'Y={position.y:.2f}'
            )

            self.get_logger().info(
                f'Linear velocity: {velocity.linear.x:.2f} m/s'
            )

            self.get_logger().info(
                f'Angular velocity: {velocity.angular.z:.2f} rad/s'
            )
        else:
            self.get_logger().warn('Waiting for Odometry data')

        if self.imu is not None:

            acceleration = self.imu.linear_acceleration

            self.get_logger().info(
                f'IMU Acceleration: '
                f'X={acceleration.x:.2f}, '
                f'Y={acceleration.y:.2f}, '
                f'Z={acceleration.z:.2f}'
            )
        else:
            self.get_logger().warn('Waiting for IMU data')


def main(args=None):

    rclpy.init(args=args)
    node = SensorMonitor()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()

        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
