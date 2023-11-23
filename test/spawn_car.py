#!/usr/bin/env python3

import sys
import rclpy
from gazebo_msgs.srv import SpawnEntity
from geometry_msgs.msg import Pose

def main():
    rclpy.init()
    node = rclpy.create_node('spawn_car_node')
    client = node.create_client(SpawnEntity, '/spawn_entity')
    node.get_logger().info("Waiting for Gazebo's spawn_entity service...")

    while not client.wait_for_service(timeout_sec=1.0):
        if not rclpy.ok():
            node.get_logger().info("Node interrupted. Exiting...")
            return
        node.get_logger().info("Service not available, waiting again...")

    node.get_logger().info("Gazebo's spawn_entity service is available.")

    # List of car names to spawn
    car_names = ['PR001', 'PR002']

    for car_name in car_names:
        request = SpawnEntity.Request()
        request.name = car_name
        request.xml = open("/home/ros2/Ros2Projects/oom_ws/src/ros2_term_project/models/prius_hybrid.sdf", 'r').read()
        request.initial_pose = Pose()
        request.initial_pose.position.x = 93.0
        request.initial_pose.position.y = -11.7 if car_name == 'PR002' else -15.9
        request.initial_pose.orientation.z = -1.57

        future = client.call_async(request)
        rclpy.spin_until_future_complete(node, future)

        if future.result() is not None:
            node.get_logger().info(f"Entity spawned: {car_name}")
        else:
            node.get_logger().error(f"Failed to spawn entity: {car_name}")

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
