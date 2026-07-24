# ROS1-Based Multi-Sensor Monitoring System for Industrial Robot

## Overview

This project develops a real-time sensor acquisition and processing framework
for industrial robotic systems.

The system integrates a vibration sensor (HU108) and an IMU sensor
(CZ028 IM948) with ROS1 to collect, synchronize, process, and visualize
robot-related physical data.

The final goal is to connect sensor feedback with a KUKA industrial robot
platform for condition monitoring and predictive maintenance applications.

## Hardware

- HU108 three-axis vibration sensor
- CZ028 IM948 IMU sensor
- Arduino / STM32 (to be added)
- KUKA industrial robot

## Objectives

- Acquire real-time vibration data
- Acquire IMU motion data
- Timestamp sensor measurements
- Publish sensor data through ROS topics
- Process signals using filtering and frequency analysis
- Synchronize sensor data with robot joint states
- Visualize robot condition information

## System Architecture

```
Sensor
  ↓
Microcontroller
  ↓
ROS Driver Node
  ↓
ROS Topics
  ↓
Data Processing Node
  ↓
Visualization / Analysis
```

See [docs/system_architecture.md](docs/system_architecture.md) for details.

## Repository Structure

```
ROS-KUKA-Sensor-Monitoring
├── README.md
├── docs
│   ├── system_architecture.md
│   ├── sensor_protocol.md
│   └── experiment_log.md
├── hardware
│   ├── HU108
│   │   ├── datasheet.md
│   │   ├── communication.md
│   │   └── test_data.csv
│   └── CZ028_IM948
│       ├── datasheet.md
│       ├── communication.md
│       └── test_data.csv
├── ros_ws
│   └── src
│       ├── hu108_driver
│       ├── imu_driver
│       └── sensor_fusion
├── analysis
│   ├── fft.py
│   ├── filtering.py
│   └── visualization.py
└── demos
    └── video.mp4
```

## Development Environment

- Ubuntu 20.04
- ROS Noetic
- Python 3
- C++
- Arduino / STM32
- KUKA ROS package

## Roadmap

- [x] Hardware selection
- [ ] Sensor communication (HU108 serial read + CSV logging)
- [ ] ROS publisher node (HU108)
- [ ] Timestamp synchronization
- [ ] IMU integration (CZ028 IM948)
- [ ] Signal processing (filtering, FFT)
- [ ] KUKA joint-state synchronization
- [ ] Anomaly / condition-monitoring demo

## License

TBD

## Contact

TBD
# ROS-based-Multi-Sensor
