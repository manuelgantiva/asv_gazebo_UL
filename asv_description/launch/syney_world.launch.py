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

    urdf_path = os.path.join(this_pkg, 'urdf', 'asv_loyola.urdf.xacro')
    rviz_config_path = os.path.join(this_pkg, 'rviz', 'urdf_config.rviz')
    
    launch_gz_sim_empty = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([
                PathJoinSubstitution([
                    FindPackageShare('vrx_gz'),
                    'launch',
                    'competition.launch.py'
                ])
            ]),
            launch_arguments={
                'world': 'sydney_regatta'
            }.items()
        )
    
    robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[
            {'use_sim_time': True},
            {'robot_description': robot_description},
        ]
    )

    gz_create_entity = Node(
        package="ros_gz_sim",
        executable="create",
        arguments=['-topic', 'robot_description',
               '-entity', 'asv_loyola',
               '-x', '-532.0',
               '-y', '158.0',
               '-z', '0.26',
               '-Y', '-1.57'
               ]
    )

    # Bridge
    bridge_gz_node = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        parameters=[{
            'config_file': os.path.join(this_pkg, 'config', 'ros_gz_bridge.yaml'),
            'qos_overrides./tf_static.publisher.durability': 'transient_local',
        }],
        output='screen'
    )

    depth_cam_data2cam_link_tf = Node(package='tf2_ros',
                     executable='static_transform_publisher',
                     name='cam3Tolink',
                     output='log',
                     arguments=['0.0', '0.0', '0.0', '0.0', '0.0', '0.0',
                                'asv_camera','asv_loyola/base_link/camera_link_optical'])

    rviz2_node = Node(
        package="rviz2",
        executable="rviz2",
        arguments=['-d', rviz_config_path]
    )

    ld.add_action(launch_gz_sim_empty)
    ld.add_action(robot_state_publisher_node)
    ld.add_action(gz_create_entity)
    ld.add_action(bridge_gz_node)
    ld.add_action(depth_cam_data2cam_link_tf)
    ld.add_action(rviz2_node)
    return ld


