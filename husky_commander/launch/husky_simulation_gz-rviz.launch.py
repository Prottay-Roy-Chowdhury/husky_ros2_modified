from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    declared_arguments = [
        DeclareLaunchArgument(
            "type",
            default_value="husky_basic",
            choices=["husky_basic", "husky_manipulator", "husky_ur"],
            description="Robot model/config folder name",
        ),
        DeclareLaunchArgument(
            "rviz",
            default_value="true",
            choices=["true", "false"],
            description="Launch RViz",
        ),
        DeclareLaunchArgument(
            "world",
            default_value="warehouse",
            description="Gazebo world",
        ),
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="true",
            choices=["true", "false"],
            description="Use simulation time",
        ),
        DeclareLaunchArgument(
            "generate",
            default_value="true",
            choices=["true", "false"],
            description="Generate Clearpath files before spawning",
        ),
    ]

    robot_type = LaunchConfiguration("type")
    rviz = LaunchConfiguration("rviz")
    world = LaunchConfiguration("world")
    use_sim_time = LaunchConfiguration("use_sim_time")
    generate = LaunchConfiguration("generate")

    setup_path = PathJoinSubstitution([
        "/dev_ws/src/husky_commander/config",
        robot_type,
    ])

    husky_simulation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare("clearpath_gz"),
                "launch",
                "simulation.launch.py",
            ])
        ),
        launch_arguments={
            "setup_path": setup_path,
            "rviz": rviz,
            "world": world,
            "use_sim_time": use_sim_time,
            "generate": generate,
        }.items(),
    )

    return LaunchDescription(declared_arguments + [husky_simulation_launch])