import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from .line_tracker import LineTracker
import cv_bridge
import time


class LineFollower(Node):
    def __init__(self, line_tracker: LineTracker):
        super().__init__('line_follower')
        self.line_tracker = line_tracker
        self.bridge = cv_bridge.CvBridge()
        self._subscription = self.create_subscription(Image, '/camera1/image_raw', self.image_callback, 10)
        self._publisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.twist = Twist()
        self.twist.linear.x = 1.0
        self.img = None
        self.start_time = time.time()
        self.current_speed = self.twist.linear.x

    def image_callback(self, msg: Image):
        img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        self.line_tracker.process(img)

        self.twist.angular.z = (-1) * self.line_tracker.delta / 450  # OK: 400
        self.current_speed = self.twist.linear.x
        self.get_logger().info('angular.z = %f, %3f m/s' % (self.twist.angular.z, self.current_speed))
        self._publisher.publish(self.twist)

    def stop(self):
        self.twist.linear.x = 0.0
        self.twist.angular.z = 0.0
        self._publisher.publish(self.twist)

    @property
    def publisher(self):
        return self._publisher


def main():
    rclpy.init()
    tracker = LineTracker()
    follower = LineFollower(tracker)
    try:
        rclpy.spin(follower)
    except KeyboardInterrupt:
        follower.stop()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
