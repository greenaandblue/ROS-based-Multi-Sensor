# CZ028 IM948 Communication Protocol

> Fill this in once the physical interface and output mode are confirmed.

## Interface

- Physical layer: TBD (UART / I2C / SPI)
- Baud rate: TBD
- Output mode: TBD (raw accel/gyro vs. fused quaternion/Euler)
- Output rate: TBD

## Data Subset Used by This Project

| Field | Source | Notes |
|-------|--------|-------|
| linear_acceleration.x/y/z | accelerometer | raw or filtered |
| orientation (quaternion) | onboard fusion | preferred over raw gyro+mag |
| header.stamp | ROS node | assigned at read time |

## Read Script Skeleton

```python
import serial
import time

PORT = "/dev/ttyUSB1"   # TBD - confirm actual port
BAUD = 115200            # TBD - confirm actual baud rate

def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if not line:
            continue
        # TODO: replace with real frame parsing once protocol is confirmed
        print(line)

if __name__ == "__main__":
    main()
```

## Next Step: ROS Node

Wrap this inside `ros_ws/src/imu_driver`, publishing `sensor_msgs/Imu` on
`/imu/data` with a properly stamped `Header`.
