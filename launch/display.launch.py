from os.path import sep, join
from tempfile import gettempdir

from ament_index_python.packages import get_package_share_directory, get_package_prefix
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    urdf = [
        get_package_share_directory('urdf_tutorial'),
        sep,
        LaunchConfiguration('model', default='urdf/01-myfirst.urdf')
    ]

    parsed_urdf = join(gettempdir(), 'parsed.urdf')  # Robot State Publisher 2 requires a file

    return LaunchDescription([
        DeclareLaunchArgument(
            'model',
            default_value='urdf/01-myfirst.urdf'
        ),
        DeclareLaunchArgument(
            'gui',
            default_value='true'
        ),
        DeclareLaunchArgument(
            'rvizconfig',
            default_value=join(get_package_share_directory('urdf_tutorial'), 'rviz', 'urdf.rviz')
        ),
        ExecuteProcess(
            cmd=[get_package_prefix('xacro') + '/bin/xacro', urdf, '-o', parsed_urdf],
            output='screen',
            on_exit=[
                Node(
                    package='robot_state_publisher',
                    node_executable='robot_state_publisher',
                    node_name='robot_state_publisher',
                    output='screen',
                    arguments=[parsed_urdf]
                ),
            ]
        ),
        Node(
            node_name='joint_state_publisher',
            package='joint_state_publisher_gui',
            node_executable='joint_state_publisher_gui',
            output='screen',
            condition=IfCondition(LaunchConfiguration("gui"))
        ),
        Node(
            node_name='joint_state_publisher',
            package='joint_state_publisher',
            node_executable='joint_state_publisher',
            output='screen',
            condition=UnlessCondition(LaunchConfiguration("gui"))
        ),
        Node(
            package='rviz2',
            node_executable='rviz2',
            output='screen',
            arguments=['-d', LaunchConfiguration('rvizconfig')]
        ),

    ])
