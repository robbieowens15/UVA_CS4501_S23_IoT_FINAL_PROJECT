# Final Project for Internet of Things (IoT) CS 4501 Spring 23 - Group 11

### LoRaReceiver + GPS: 
Code to run on Heltec v3 board, publishes GPS and Battery Level data to MQTT
    Note: Battery level is simulated in ROS

### ROS: 
Docker Image to run lightweight ROS imagine for proof of concept or IoT --> ROS service calls

### webserver:
front end GUI to see metrics and provision downstream commands; backend to publish downstream commands to ROS Robot via MQTT  

Documentation for how to acquire the data. (webhooks recommended)
https://www.thethingsindustries.com/docs/integrations/

How to queue a response back to device for (for ACK and Downlink path)?