from setuptools import setup
import os
from glob import glob

package_name = 'battery_monitor'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name), glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='rao7utn@virginia.edu',
    description='UVA CS 4501 Internet of Things Final Project: Simulated ROS Battery',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'battery_monitor_node = battery_monitor.battery_monitor_node:main'
        ],
    },
)