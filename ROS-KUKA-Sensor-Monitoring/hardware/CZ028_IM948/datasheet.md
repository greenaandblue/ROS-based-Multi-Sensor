# CZ028 IM948 IMU Sensor

## Purpose in This Project

Second-stage sensor, introduced after the HU108 vibration pipeline works.
Provides orientation/motion data for the robot, feeding into sensor fusion
with the vibration data and (eventually) KUKA joint states.

## Full Sensor Capabilities (module supports, but not all used)

- Accelerometer
- Gyroscope
- Magnetometer
- Quaternion output
- Euler angle output
- Barometer

## What This Project Actually Uses

To keep scope manageable, only the following are used:

- Acceleration
- Orientation quaternion
- Timestamp

## Key Specs

> Fill in from the vendor datasheet:

| Parameter | Value |
|-----------|-------|
| Output interface | TBD (UART / I2C / SPI) |
| Baud rate | TBD |
| Output rate | TBD |
| Power supply | TBD |

## ROS Integration Target

Publish to the standard topic:

```
/imu/data   (sensor_msgs/Imu)
```

This keeps the door open to using standard ROS packages (e.g.
`robot_localization`) for later fusion work, instead of a fully custom
message type.

See [communication.md](communication.md) for protocol details.
