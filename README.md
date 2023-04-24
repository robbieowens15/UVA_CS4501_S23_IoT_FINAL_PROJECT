# Final Project for Internet of Things (IoT) CS 4501 Spring 23 - Group 11

## Description of Contents
LoRaReceiver: Code to run on Heltec v3 board, publishes GPS and Battery Level data to MQTT
ROS: Docker Image to run lightweight ROS imagine for proof of concept of LoRaReceiver sending service calls to ROS Robot
webserver: front end GUI to see metrics and provision downstream commands; backend to publish downstream commands to ROS Robot via MQTT  