import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

def generate_launch_description():
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Config files directory      
    lpslam_config_dir = os.path.join(get_package_share_directory('turtlebot3_lpslam'), 'config')

    return LaunchDescription([
        # lpslam
        Node(
            package='lpslam',
            #namespace='lpslam',
            executable='lpslam_node',
            name='lpslam_compute',
            output='screen',
            emulate_tty=True,
            parameters=[
                {"use_sim_time" : True},
                {"laserscan_frame_id" : 'base_scan'},
                {"lpslam_config": os.path.join(lpslam_config_dir, 'gazebo_openvslam_tb3.json')},
                {"write_lpslam_log" : True}
            ],

            arguments= [
                '--ros-args', '--log-level', 'INFO'
            ],
            remappings=[
                ('left_image_raw', 'stereo_camera/left/image_raw'),
                ('right_image_raw', 'stereo_camera/right/image_raw')
            ]
        ),
        # rviz
        Node(
                package = 'rviz2',
                executable = 'rviz2',
                name = 'rviz2',
                arguments = [ '-d', os.path.join(lpslam_config_dir, 'lpslam.rviz')],   
                output = 'screen')
    ])
