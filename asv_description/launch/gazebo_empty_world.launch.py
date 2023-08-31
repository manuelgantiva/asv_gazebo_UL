from launch import LaunchDescription
from launch_ros.actions import Node

# Exec robot description node with xacro
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command

# Utilizing launch files from other packages
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch import LaunchDescription
from launch.substitutions import PathJoinSubstitution

# Retrieving path information 
from ament_index_python.packages import get_package_share_directory
from pathlib import Path 

# Retrieving path information 
import os
from ament_index_python.packages import get_package_share_path

def generate_launch_description():
    ld = LaunchDescription()

    this_pkg = get_package_share_directory("asv_description")

    simulation_world_file_path = Path(this_pkg, "worlds/test_world.world").as_posix()

    urdf_path = os.path.join(this_pkg, 'urdf', 'asv_loyola.urdf.xacro')
    rviz_config_path = os.path.join(this_pkg, 'rviz', 'urdf_config.rviz')
    
    launch_gz_sim_empty = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('ros_gz_sim'),
                    'launch',
                    'gz_sim.launch.py'
                ])
            ]),
            launch_arguments={
                'gz_args': 'empty.sdf'
            }.items()
        )
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{'robot_description': robot_description}]
    )

    gz_create_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=['-topic', 'robot_description',
               '-entity', 'my_robot',
               '-x', '0.0',
               '-y', '0.0',
               '-z', '0.26']
    )


    joint_state_publisher_gui_node = Node(
        package="joint_state_publisher_gui",
        executable="joint_state_publisher_gui"
    )

    bridge_gz_node = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '/world/empty/model/asv_loyola/joint_state@'
                'sensor_msgs/msg/JointState[gz.msgs.Model',
                '/model/asv_loyola/joint/left_motor_joint/cmd_thrust@'
                'std_msgs/msg/Float64]gz.msgs.Double',
                '/model/asv_loyola/joint/right_motor_joint/cmd_thrust@'
                'std_msgs/msg/Float64]gz.msgs.Double'
            ],
            remappings=[
                ('/world/empty/model/asv_loyola/joint_state', '/joint_states'),
                ('/model/asv_loyola/joint/left_motor_joint/cmd_thrust', '/thrust_left'),
                ('/model/asv_loyola/joint/right_motor_joint/cmd_thrust', '/thrust_right')
            ]
        )


    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    ld.add_action(launch_gz_sim_empty)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(gz_create_entity)
    ld.add_action(bridge_gz_node)
    ld.add_action(rviz2_node)
    return ld