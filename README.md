# Mobile IMU Telemetry Controller for TurtleBot3

Control a TurtleBot3 robot in Gazebo using real-time IMU sensor data streamed from an Android smartphone over UDP.

This project was developed as part of the **CROB Robotics Team – Phase 2 Recruitment Task** under the **Robotics Systems, Simulation & Control Domain**.

---

## Overview

The system transforms an Android smartphone into a wireless motion controller for a TurtleBot3 robot. IMU data (Accelerometer, Gyroscope, and Magnetometer) is transmitted via UDP to a ROS 2 node running on Ubuntu. The node processes the incoming sensor values and converts them into velocity commands (`Twist` messages) that drive the robot inside a Gazebo simulation.

---

## System Architecture

```text
[Android Smartphone]
       │
       │ Raw IMU Data
       │ (Accel, Gyro, Mag)
       │ UDP Stream (Port 1212)
       ▼
[Ubuntu 22.04 Workstation]
       │
       │ ROS 2 Python Node
       │ Data Parsing & Kinematics
       ▼
[ROS 2 Topic: /cmd_vel]
       │
       │ Twist Messages
       ▼
[Gazebo Simulation]
       │
       ▼
[TurtleBot3 Robot]
```

---

## Prerequisites

### Operating System

* Ubuntu 22.04 LTS

### ROS Distribution

* ROS 2 Humble Hawksbill

### Simulator

* Gazebo 11

### Required Packages

```bash
sudo apt install ros-humble-gazebo-ros-pkgs
sudo apt install ros-humble-turtlebot3
sudo apt install ros-humble-turtlebot3-gazebo
```

### Mobile Application

* VirtualIMU APK (Android)

---

## Project Structure

```text
mobile_imu_control/
├── mobile_imu_control/
│   ├── teleop_node.py
│   └── __init__.py
├── package.xml
├── setup.py
├── setup.cfg
└── README.md
```

---

## Installation

### 1. Clone into ROS 2 Workspace

```bash
cd ~/crob_ws/src

git clone https://github.com/ras-al/Mobile-IMU-Telemetry-Controller-for-TurtleBot3
```

---

### 2. Build the Package

```bash
cd ~/crob_ws

colcon build --packages-select mobile_imu_control

source install/setup.bash
```

---

## Network Configuration

Ensure that:

* Your Ubuntu workstation and Android phone are connected to the same Wi-Fi network.
* UDP port **1212** is open.

Allow incoming UDP traffic:

```bash
sudo ufw allow 1212/udp
```

Find your workstation IP address:

```bash
ip addr show
```

Example:

```text
192.168.1.101
```

This IP address must be entered in the VirtualIMU application.

---

## Running the System

### Terminal 1 — Launch Gazebo

```bash
export TURTLEBOT3_MODEL=burger

ros2 launch turtlebot3_gazebo empty_world.launch.py
```

---

### Terminal 2 — Launch Telemetry Node

```bash
source install/setup.bash

ros2 run mobile_imu_control teleop_node
```

---

### On Your Android Device

1. Open the VirtualIMU app.
2. Enter:

   * PC IP Address
   * Port: `1212`
3. Press **Start UDP Stream**.
4. Tilt the phone to control the robot.

---

## Control Mapping

| Phone Motion  | Robot Action  |
| ------------- | ------------- |
| Tilt Forward  | Move Forward  |
| Tilt Backward | Move Backward |
| Tilt Left     | Rotate Left   |
| Tilt Right    | Rotate Right  |
| Phone Flat    | Stop          |

---

## Features

### Real-Time UDP Telemetry

* Receives IMU data wirelessly from Android.
* Low-latency communication using UDP sockets.

### ROS 2 Integration

* Native ROS 2 Python node.
* Publishes velocity commands directly to `/cmd_vel`.

### TurtleBot3 Simulation

* Fully integrated with Gazebo.
* No physical robot required.

### Coordinate Frame Correction

Android devices use a different sensor coordinate frame than differential-drive robots.

The node includes:

* Axis remapping
* Sign correction
* Velocity scaling

to ensure intuitive control behavior.

---

## Progress Gallery (video might be lag because of converted to GIF)

![alt text](<src/mobile_imu_control/resource/Screencast from 06-21-2026 12_29_33 PM.gif>)

## Challenges Solved

### 1. Real-Time Mobile-to-ROS Communication

Successfully bridged an external Android device with a ROS 2 environment using UDP networking.

### 2. Sensor Axis Alignment

Android IMU axes differ from standard robot kinematic frames.

Implemented:

* Axis transformation
* Sign inversion
* Motion calibration

for accurate robot control.

### 3. Velocity Scaling

Mapped raw sensor values to safe robot velocities suitable for TurtleBot3 operation.

---

## Week 3 Roadmap

### 🔹 Sensor Filtering

Implement a Simple Moving Average (SMA) filter:

```text
Raw IMU → SMA Filter → Velocity Mapping
```

Benefits:

* Reduced jitter
* Smoother movement
* Improved control stability

---

### 🔹 Deadzone Implementation

Create a configurable deadzone around neutral phone orientation.

Benefits:

* Prevent unintended drift
* Robot remains stationary when phone is held flat

---

## Technologies Used

* ROS 2 Humble
* Python 3
* Gazebo 11
* TurtleBot3
* UDP Networking
* Linux (Ubuntu 22.04)
* Android IMU Sensors

---

## Author

**Rasal Musthafa**
B.Tech Computer Science & Engineering
TKM College of Engineering, Kollam

Developed for the **CROB Robotics Team Recruitment Task (Phase 2)**.

---
