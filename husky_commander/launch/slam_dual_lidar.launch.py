from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    front_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="front_lidar_bridge",
        output="screen",
        arguments=[
            "/a200_0000/sensors/lidar2d_0/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan"
        ],
        parameters=[{"use_sim_time": True}],
    )

    rear_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="rear_lidar_bridge",
        output="screen",
        arguments=[
            "/a200_0000/sensors/lidar2d_1/scan@sensor_msgs/msg/LaserScan[gz.msgs.LaserScan"
        ],
        parameters=[{"use_sim_time": True}],
    )

    dual_merger = Node(
        package="dual_laser_merger",
        executable="dual_laser_merger_node",
        name="dual_laser_merger",
        output="screen",
        parameters=[
            {
                "use_sim_time": True,
                "laser_1_topic": "/a200_0000/sensors/lidar2d_0/scan",
                "laser_2_topic": "/a200_0000/sensors/lidar2d_1/scan",
                "merged_topic": "/merged",
                "target_frame": "base_link",
                "qos_overrides./merged.publisher.reliability": "reliable",
            }
        ],
        remappings=[
            ("/tf", "/a200_0000/tf"),
            ("/tf_static", "/a200_0000/tf_static"),
        ],
    )

    slam_toolbox = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[
            "/opt/ros/humble/share/slam_toolbox/config/mapper_params_online_async.yaml",
            {
                "use_sim_time": True,
                "scan_topic": "/merged",
            },
        ],
        remappings=[
            ("/tf", "/a200_0000/tf"),
            ("/tf_static", "/a200_0000/tf_static"),
        ],
    )

    return LaunchDescription([
        front_bridge,
        rear_bridge,
        dual_merger,
        slam_toolbox,
    ])