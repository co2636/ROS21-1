#!/usr/bin/env python3

import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess, DeclareLaunchArgument

# Create a LaunchDescription
ld = LaunchDescription()

def generate_launch_description():
    # Get the absolute path of the world file
    world_file_name = 'car_track.world'
    world_path = os.path.join(get_package_share_directory('ros2_term_project'), 'worlds', world_file_name)

    # Declare a launch argument for using simulation time
    use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true'
    )

    # Launch Gazebo with the specified world file
    gazebo_run = ExecuteProcess(
        cmd=['gazebo', '-s', 'libgazebo_ros_factory.so', world_path],
        output='screen',
        additional_env={
            'GAZEBO_MODEL_PATH': '/home/ros2/Ros2Projects/oom_ws/src/ros2_term_project/models',
        }
    )

    # Add the declared argument and Gazebo process to the launch description
    ld.add_action(use_sim_time)
    ld.add_action(gazebo_run)

    # Spawn the selected cars using the modified spawn_car.py script
    spawn_cars_node = Node(
        package='ros2_term_project',
        executable='/home/ros2/Ros2Projects/oom_ws/src/ros2_term_project/test/spawn_car.py',  # Modified script name
        output='screen'
    )

    # Add the spawn_cars_node to the launch description
    ld.add_action(spawn_cars_node)

    return ld
