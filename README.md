# Final Project for Internet of Things (IoT) CS 4501 Spring 23 - Group 11

# Documentation for the motivation of this project:
[Google Slides - Presentation Deck](https://docs.google.com/presentation/d/1wdEMc5fuZC-7Zq7lYcGgHamXlNqLyQfKI4Hl6TadLBU/edit?usp=sharing)
- Motivation
- Technical Design Diagram
- Demo
[Google Docs - Motivation and Technical Abstract](https://docs.google.com/document/d/1cnuJvqSw01UkA69GmqIJAPXp1Xdtyoxjug-z762RAZE/edit?usp=sharing)
- Links to all required resources for project setup

# Overview of Codebase
## `LoRaGPS Transmitter/LoRaWAN`
Contains the code for the Heltec Board to read GPS data off a hardware serial then transmit the data over LoRa transmitter

## `SimpleGPS`
Contains the code only read GPS data via hardware serial on Heltec board
(Intended to help others bootstrap projects more rapidly)  

## `robot`
INCOMPLETE!!
Goal was to have ROS code simulate a battery then the Heltec board would make ROS service calls to retrieve this data. Ended up being too difficult to make service call requests on a ROS client (running on Heltec board) from outside the ROS docker container

This Folder has extensive documentation for setting up the ROS docker container
`robot/mnt/project_ws` is where battery was simulated
`robot/mnt/ros2_sandbox_ws` is where ROS2 tutorials were conducted to figure out service calls
The file `robot/README.md` has more explicit instructions

## `web`
This folder contains both the front and backend of our web service. In the root there is a flask Server (`web/Server.py`) file that is responsible for the entire backend connection to TTN and battery simulator. The frontend folder (`web/frontend/`)  contains the React project which connects to the Google Maps API and presents the user with the visualization of the data.
