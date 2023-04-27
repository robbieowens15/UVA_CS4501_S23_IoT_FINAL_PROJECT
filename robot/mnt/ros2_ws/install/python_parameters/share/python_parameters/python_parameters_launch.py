from launch import LaunchDescription
from launch_ros.actions import Node

import sys

def generate_launch_description():
    for arg in sys.argv:
        if arg.startswith("battery_time:="):
            value = arg.split(":=")[1]
        else:
            value = '100'

    return LaunchDescription([
        Node(
            package='python_parameters',
            executable='minimal_param_node',
            name='custom_minimal_param_node',
            output='screen',
            emulate_tty=True,
            parameters=[
                {'battery_time': value}
            ]
        )
    ])