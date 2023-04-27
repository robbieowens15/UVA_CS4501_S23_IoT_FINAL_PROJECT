Using official ROS Docker image: https://hub.docker.com/_/ros

## Setup
Steps for setup (assume docker desktop installed and running)

```
docker pull ros

# Note, this docker file is not need rn, but as we change the container
(e.g. install libraries, change networking settings, etc)
We can edit and append this file to create new Docker images (thus spinning up)
containers which fulfill our changing requirements
--------------------------------------------------------------------------------
cat Dockerfile
FROM ros:foxy

# install ros package
RUN apt-get update && apt-get install -y \
      ros-${ROS_DISTRO}-demo-nodes-cpp \
      ros-${ROS_DISTRO}-demo-nodes-py && \
    rm -rf /var/lib/apt/lists/*

# launch ros package
CMD ["ros2", "launch", "demo_nodes_cpp", "talker_listener.launch.py"]
--------------------------------------------------------------------------------

#Create location on host file system for mount:
mkdir ./mnt/

#start ROS container
docker run -d \
-it \
--name mower \
--mount type=bind,source="$(pwd)"/mnt,target=/root/mnt \
ros

#lookup name of the ROS container
#N.B. Must open a NEW TERMINAL SESSION ON HOST MACHINE
docker ps -l
#e.g. output
CONTAINER ID   IMAGE     COMMAND                  CREATED         STATUS         PORTS     NAMES
9699b018e4cc   ros       "/ros_entrypoint.sh …"   3 minutes ago   Up 3 minutes             mower

#stop ROS container
docker stop mower

#start docker container
docker start mower

#start a new terminal session within container (FROM HOST MACHINE SHELL)
docker exec -it mower bash
```

Notes for future: 
- may be useful to open port for ROS service calls
- if (above) too complete, place "systems calls" as files in mnt

### Configuring the Ubuntu OS in the container to run ROS2

following: http://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
- I followed this tutorial through and verified setup in the pub-sub at bottom of the page
Note, by following this I have warning about two ROS installs

```
sudo apt update

W: Target Packages (main/binary-amd64/Packages) is configured multiple times in /etc/apt/sources.list.d/ros2-latest.list:1 and /etc/apt/sources.list.d/ros2.list:1
W: Target Packages (main/binary-all/Packages) is configured multiple times in /etc/apt/sources.list.d/ros2-latest.list:1 and /etc/apt/sources.list.d/ros2.list:1
W: Target Packages (main/binary-amd64/Packages) is configured multiple times in /etc/apt/sources.list.d/ros2-latest.list:1 and /etc/apt/sources.list.d/ros2.list:1
W: Target Packages (main/binary-all/Packages) is configured multiple times in /etc/apt/sources.list.d/ros2-latest.list:1 and /etc/apt/sources.list.d/ros2.list:1
W: Target Packages (main/binary-amd64/Packages) is configured multiple times in /etc/apt/sources.list.d/ros2-latest.list:1 and /etc/apt/sources.list.d/ros2.list:1
W: Target Packages (main/binary-all/Packages) is configured multiple times in /etc/apt/sources.list.d/ros2-latest.list:1 and /etc/apt/sources.list.d/ros2.list:1
```

Now after this setup is it possible to source correctly via:
`source /opt/ros/humble/setup.bash`

### Building the workspace
following this tutorial: http://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Colcon-Tutorial.html

## Creating the Simulated Mover Robot

Following this guide to create simple Python pub/sub: http://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html

And this guide on service calls: http://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html

Setting up the ROS project to receive system parameters



## todo
creating new service calls: (useful for receiving GPS coordinates)
http://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Custom-ROS2-Interfaces.html

possible solution to communicating through docker container
https://github.com/uts-magic-lab/rosduct


## Cleanup
'''
docker rm mower
'''

other useful commands found here:
https://tuw-cpsg.github.io/tutorials/docker-ros/