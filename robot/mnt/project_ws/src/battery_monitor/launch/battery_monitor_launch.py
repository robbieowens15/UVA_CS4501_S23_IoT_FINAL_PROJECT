from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='battery_monitor',
            executable='battery_monitor_node',
            name='battery_monitor_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'battery_time': "100"} #100s to depletion
            ]
        )
    ])