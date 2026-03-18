from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package="slam_toolbox",
            executable="async_slam_toolbox_node",
            name="slam_toolbox",
            output="screen",
            parameters=[
                "/opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml",
                {
                    "use_sim_time": True,
                    "scan_topic": "/a200_0000/sensors/lidar2d_0/scan",
                },
            ],
            remappings=[
                ("/tf", "/a200_0000/tf"),
                ("/tf_static", "/a200_0000/tf_static"),
            ],
        )
    ])