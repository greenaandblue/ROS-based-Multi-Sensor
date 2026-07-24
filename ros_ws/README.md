# ros_ws

This will become the ROS1 catkin workspace once Phase 2 begins
(see `docs/system_architecture.md`, section 6).

Planned package layout:

```
ros_ws/src
├── hu108_driver
│   ├── scripts/hu108_node.py
│   ├── launch/hu108.launch
│   └── msg/Vibration.msg
├── imu_driver
│   ├── scripts/imu_node.py
│   ├── launch/imu.launch
│   └── msg/ (uses sensor_msgs/Imu)
└── sensor_fusion
    ├── scripts/fusion_node.py
    └── launch/fusion.launch
```

`Vibration.msg` (draft, currently at repo root of this folder for reference)
will move into `hu108_driver/msg/` once the catkin package is created.

Not yet created — placeholder until Phase 1 (serial read + CSV logging,
see `hardware/HU108/communication.md`) is validated.
