import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Config files directory      
    lpslam_config_dir = os.path.join(get_package_share_directory('turtlebot3_lpslam'), 'config')
    params = os.path.join(lpslam_config_dir, 'lpslam_params.yaml') 

    return LaunchDescription([
        # lpslam
        Node(
            package='lpslam',
            executable='lpslam_node',
            name='lpslam_node',
            output='screen',
            emulate_tty=True,
            parameters=[params],

            arguments= [
                '--ros-args', '--log-level', 'INFO'
            ],
        ),
        # rviz
        Node(
                package = 'rviz2',
                executable = 'rviz2',
                name = 'rviz2',
                arguments = [ '-d', os.path.join(lpslam_config_dir, 'lpslam.rviz')],   
                output = 'screen')
    ])
