source /opt/ros/humble/setup.bash
source /opt/ros/humble/setup.bash
cd /root/mnt/project_ws
colcon build --packages-select python_parameters
source install/setup.bash
ls
cd ../
ls
cd ros2_sandbox_ws/
ls
ls src
cd src/
ros2 pkg create --build-type ament_python py_pubsub
cd py_pubsub/py_pubsub/
wget https://raw.githubusercontent.com/ros2/examples/humble/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py
sudo apt install wget
wget https://raw.githubusercontent.com/ros2/examples/humble/rclpy/topics/minimal_publisher/examples_rclpy_minimal_publisher/publisher_member_function.py
wget https://raw.githubusercontent.com/ros2/examples/humble/rclpy/topics/minimal_subscriber/examples_rclpy_minimal_subscriber/subscriber_member_function.py
rosdep install -i --from-path src --rosdistro humble -y
cd ../../
ls
ros2 pkg create --build-type ament_python py_srvcli --dependencies rclpy example_interfaces
cd ../
rosdep install -i --from-path src --rosdistro humble -y
colcon build --packages-select py_srvcli
source install/setup.bash
ros2 run py_srvcli service
source install/setup.bash
ros2 run py_srvcli service
colcon build --packages-select py_srvcli
ros2 run py_srvcli service
exit
cd root/mnt/
ls
cd ros2_sandbox_ws/
ls
cd src/
ls
rosdep install -i --from-path src --rosdistro humble -y
cd ../
rosdep install -i --from-path src --rosdistro humble -y
source install/setup.bash
ros2 run py_srvcli service
colcon build --packages-select py_srvcli
source install/setup.bash
ros2 run py_srvcli service
exit
ros2 run py_srvcli client 2 3
source /opt/ros/humble/setup.bas
source /opt/ros/humble/setup.bash
ros2 run py_srvcli client 2 3
ros2 run py_srvcli client 2 3
cd /root/mnt/ros2_sandbox_ws/
ls
source install/setup.bash
ros2 run py_srvcli service
ros2 run py_srvcli client 2 3
ros2 run py_srvcli client 2 3
ros2 run py_srvcli client 2 4
exit
