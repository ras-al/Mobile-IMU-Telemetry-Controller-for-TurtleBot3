# Mobile IMU Telemetry Controller for TurtleBot3

This repository contains a **ROS 2 (Humble)** package designed to control a TurtleBot3 in a Gazebo simulation using real-time IMU sensor data streamed over UDP from an Android smartphone.

This project was successfully completed as part of the **CROB Robotics Team Phase 2 Recruitment Task (Robotics Systems, Simulation & Control Domain)**. All minimum requirements and bonus objectives were successfully achieved.

---

# System Architecture

```text
[Android Smartphone]
        │
        │  (Raw IMU Data via UDP Port 1212)
        ▼
[Python ROS 2 Node]
(Parsing, Calibration & Filtering)
        │
        ├────────────────────────────────────────────┐
        │                                            │
        │ (Twist Message: /cmd_vel)                  │
        ▼                                            ▼
[Gazebo Simulation]                         [rosbridge_server]
                                                     │
                                                     │ (WebSockets)
                                                     ▼
                                          [Web Telemetry Dashboard]
```

---

# Prerequisites

* **Operating System:** Ubuntu 22.04 LTS
* **Middleware:** ROS 2 Humble Hawksbill
* **Simulator:** Gazebo 11 (`ros-humble-gazebo-ros-pkgs`)
* **Robot Packages:**

  * `ros-humble-turtlebot3`
  * `ros-humble-turtlebot3-gazebo`
* **Web Bridge:** `ros-humble-rosbridge-suite`
* **Mobile Application:** VirtualIMU APK (Android)

---

# Build and Run

## 1. Network Configuration

Ensure that your PC and Android phone are connected to the **same Wi-Fi network**.

Find your PC's local IP address:

```bash
ip addr show
```

Allow UDP traffic on port **1212**:

```bash
sudo ufw allow 1212/udp
```

---

## 2. Build the ROS 2 Workspace

Clone this package into the `src` directory of your ROS 2 workspace, then build it:

```bash
cd ~/crob_ws

colcon build --packages-select mobile_imu_control

source install/setup.bash
```

---

## 3. Launch the Complete System

Open **three separate terminals**.

### Terminal 1 – Launch Gazebo

```bash
export TURTLEBOT3_MODEL=burger

ros2 launch turtlebot3_gazebo empty_world.launch.py
```

---

### Terminal 2 – Launch ROSBridge

```bash
ros2 launch rosbridge_server rosbridge_websocket_launch.xml
```

---

### Terminal 3 – Launch the IMU Telemetry Node

```bash
source ~/crob_ws/install/setup.bash

ros2 run mobile_imu_control teleop_node
```

> **Important:** Keep your phone completely flat on the table before pressing **Enter** in Terminal 3. The node performs a **2-second calibration** to determine the resting angle, which is used as the zero reference.

---

## Web Telemetry Dashboard

Open the included **`index.html`** file in your web browser to view the live telemetry dashboard.

The dashboard visualizes the robot's real-time velocity using **roslib.js** and **rosbridge_suite**.

---

# Features

* Real-time UDP communication between an Android smartphone and ROS 2.
* Motion control of TurtleBot3 using mobile IMU data.
* Automatic correction for Android sensor axis orientation.
* Simple Moving Average (SMA) filter for smooth robot motion.
* Deadzone logic to eliminate jitter while the phone is stationary.
* Automatic startup calibration to compensate for sensor offset.
* Live web-based telemetry dashboard using ROSBridge and WebSockets.

---

# Bonus Objectives Achieved

* Sensor filtering using a Simple Moving Average (SMA).
* Automatic IMU calibration during startup.
* Deadzone implementation for stable resting behavior.
* Live telemetry visualization dashboard.
* Hardware-to-ROS real-time UDP integration.

---

# Demonstration

## Figure 1

**Demonstration Video / GIF**

> Add your demonstration video or GIF link here.

---

## Figure 2

**Telemetry Dashboard with Gazebo**

> Add a screenshot showing the Web Dashboard running alongside the Gazebo simulation.

---

# Technologies Used

* ROS 2 Humble
* Python
* TurtleBot3
* Gazebo 11
* ROSBridge Suite
* WebSockets
* HTML
* CSS
* JavaScript
* roslib.js
* UDP Networking
