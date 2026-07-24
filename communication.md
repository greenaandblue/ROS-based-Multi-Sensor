# HU108 Communication Protocol

> Fill this in once the physical interface is confirmed (UART / RS485),
> baud rate, and frame format. Template below.

## Interface

- Physical layer: TBD (UART / RS485)
- Baud rate: TBD
- Data bits / parity / stop bits: TBD
- Frame format: TBD (e.g. header byte + 3x float32 + checksum)

## Read Script (Phase 1 prototype)

`hu108_test.py` responsibilities:

- Open serial connection
- Continuously read incoming frames
- Parse X / Y / Z vibration values
- Append timestamped rows to `test_data.csv`
- Live-plot the waveform with matplotlib

```python
import serial
import csv
import time
import matplotlib.pyplot as plt

PORT = "/dev/ttyUSB0"   # TBD - confirm actual port
BAUD = 115200           # TBD - confirm actual baud rate

def main():
    ser = serial.Serial(PORT, BAUD, timeout=1)
    with open("test_data.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "x", "y", "z"])

        start = time.time()
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            # TODO: replace with real parsing once frame format is known
            try:
                x, y, z = map(float, line.split(","))
            except ValueError:
                continue
            t = time.time() - start
            writer.writerow([t, x, y, z])
            f.flush()

if __name__ == "__main__":
    main()
```

## Next Step: ROS Node

Once the raw read works, wrap this logic inside `ros_ws/src/hu108_driver`,
publishing a custom `Vibration.msg` on `/vibration/data` with a proper
`Header` timestamp (see `docs/system_architecture.md`).
