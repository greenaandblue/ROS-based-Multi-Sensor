# System Architecture

## 1. Goal

Build a ROS1-based multi-sensor data acquisition and monitoring system for
an industrial robot (KUKA), integrating a vibration sensor and an IMU sensor
to support condition monitoring and, eventually, predictive maintenance.

## 2. High-Level Data Flow

```
             ┌───────────────┐
             │   HU108       │  vibration (x, y, z)
             │  (vibration)  │
             └───────┬───────┘
                     │ serial (UART/RS485, TBD)
                     ▼
             ┌───────────────┐
             │ Microcontroller│  (Arduino/STM32, optional
             │  or direct PC  │   pass-through)
             └───────┬───────┘
                     │
             ┌───────▼───────┐        ┌───────────────┐
             │ hu108_driver  │        │ imu_driver     │◄── CZ028 IM948
             │  (ROS node)   │        │  (ROS node)    │    (accel, gyro,
             └───────┬───────┘        └───────┬────────┘     quaternion)
                     │ /vibration/data                 │ /imu/data
                     └───────────────┬─────────────────┘
                                     ▼
                          ┌─────────────────────┐
                          │  sensor_fusion node │
                          │ (time sync, filter) │
                          └──────────┬──────────┘
                                     │ /robot/condition
                                     ▼
                     ┌───────────────────────────────┐
                     │ KUKA joint_state topics        │
                     │ (from KUKA ROS driver)          │
                     └───────────────┬───────────────┘
                                     ▼
                          ┌─────────────────────┐
                          │ Analysis / Viz      │
                          │ (fft.py, rviz, etc.)│
                          └─────────────────────┘
```

## 3. ROS Package Layout

```
ros_ws/src
├── hu108_driver
│   ├── scripts/hu108_node.py
│   ├── launch/hu108.launch
│   └── msg/Vibration.msg
├── imu_driver
│   ├── scripts/imu_node.py
│   ├── launch/imu.launch
│   └── msg/ (uses sensor_msgs/Imu where possible)
└── sensor_fusion
    ├── scripts/fusion_node.py
    └── launch/fusion.launch
```

## 4. Custom Message: Vibration.msg

```
Header header

float32 acceleration_x
float32 acceleration_y
float32 acceleration_z

float32 amplitude
float32 velocity
```

`Header` provides `stamp` (timestamp) and `frame_id`, which is the basis for
later synchronization with KUKA joint states.

## 5. IMU Topic

The IMU driver should publish to the standard topic:

```
/imu/data   (sensor_msgs/Imu)
```

This keeps compatibility with standard ROS packages such as
`robot_localization` for future sensor fusion work.

## 6. Development Phases

| Phase | Milestone | Notes |
|-------|-----------|-------|
| 1 | Read HU108 over serial, log to CSV, plot with matplotlib | No ROS yet |
| 2 | Wrap HU108 reading in a ROS publisher node | `hu108_driver` package |
| 3 | Add `Header` timestamp + `frame_id` | Sync foundation |
| 4 | Add CZ028 IM948 driver publishing to `/imu/data` | `imu_driver` package |
| 5 | Synchronize vibration + IMU + KUKA joint_state | `sensor_fusion` package |
| 6 | FFT / anomaly detection on synchronized data | `analysis/fft.py` |

## 7. Open Questions / TODO

- Confirm HU108 communication protocol (UART or RS485?), output data format,
  and baud rate — this determines the first driver implementation.
- Confirm CZ028 IM948 output mode (raw vs. fused quaternion/Euler) and
  update rate.
- Determine which KUKA ROS package/driver will provide `joint_state`
  (e.g. `kuka_experimental` or a vendor-specific driver).
