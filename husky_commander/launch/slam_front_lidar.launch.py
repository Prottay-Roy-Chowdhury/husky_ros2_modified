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

    # static_lidar_tf = Node(
    #     package="tf2_ros",
    #     executable="static_transform_publisher",
    #     name="fix_lidar_tf",
    #     arguments=[
    #         "0", "0", "0.1",   # xyz (adjust height if needed)
    #         "0", "0", "0",     # rpy
    #         "base_link",       # parent
    #         "lidar2d_0_laser"  # child
    #     ],
    # )

    imu_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        name="imu_bridge",
        output="screen",
        arguments=[
            "/a200_0000/sensors/imu_0/data@sensor_msgs/msg/Imu[gz.msgs.IMU"
        ],
        parameters=[{"use_sim_time": True}],
    )

    slam_toolbox = Node(
        package="slam_toolbox",
        executable="async_slam_toolbox_node",
        name="slam_toolbox",
        output="screen",
        parameters=[
            "/dev_ws/install/share/husky_commander/map_param/mapper_params_online_async.yaml",
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
    return LaunchDescription([
        front_bridge,
        # static_lidar_tf,
        imu_bridge,
        slam_toolbox,
    ])