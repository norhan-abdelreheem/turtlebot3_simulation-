import math

import rclpy
from rclpy.node import Node
from rclpy.qos import qos_profile_sensor_data
from sensor_msgs.msg import LaserScan


class ObstacleDetector(Node):

    def __init__(self):
        super().__init__('obstacle_detector')

        self.threshold = 0.30

        self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos_profile_sensor_data
        )

        self.get_logger().info('Obstacle Detector Started')

    def scan_callback(self, msg):

        front = []
        left = []
        right = []
        rear = []

        for i, distance in enumerate(msg.ranges):

            if not math.isfinite(distance):
                continue

            if not msg.range_min <= distance <= msg.range_max:
                continue

            angle = msg.angle_min + i * msg.angle_increment

            angle = math.degrees(angle)
            angle = (angle + 180) % 360 - 180

            if -30 <= angle <= 30:
                front.append(distance)

            elif 30 < angle <= 120:
                left.append(distance)

            elif -120 <= angle < -30:
                right.append(distance)

            else:
                rear.append(distance)

        self.get_logger().info('----- OBSTACLE DATA -----')

        self.check_direction('Front', front)
        self.check_direction('Left', left)
        self.check_direction('Right', right)
        self.check_direction('Rear', rear)

    def check_direction(self, direction, distances):

        if not distances:
            self.get_logger().info(
                f'{direction}: No valid reading'
            )
            return

        nearest = min(distances)

        if nearest < self.threshold:
            self.get_logger().warn(
                f'{direction}: OBSTACLE at {nearest:.2f} m'
            )
        else:
            self.get_logger().info(
                f'{direction}: Clear ({nearest:.2f} m)'
            )


def main(args=None):

    rclpy.init(args=args)
    node = ObstacleDetector()

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
