# HU108 Three-Axis Vibration Sensor

## Purpose in This Project

Used as the first-stage sensor for the project because its measurements map
directly onto industrial vibration monitoring (e.g. motor vibration on the
KUKA robot).

## Measured Quantities

- Displacement
- Velocity
- Acceleration
- Vibration amplitude (3-axis: X, Y, Z)

## Key Specs

> Fill in from the vendor datasheet:

| Parameter | Value |
|-----------|-------|
| Measurement range | TBD |
| Frequency range | TBD |
| Output interface | TBD (UART / RS485 / analog) |
| Baud rate | TBD |
| Power supply | TBD |
| Sampling rate | TBD |

## First Milestone

> Successfully read vibration sensor data and visualize the real-time
> waveform.

## Experiment Pipeline (Phase 1, no ROS)

```
HU108
  ↓
Serial output
  ↓
Python script
  ↓
CSV
  ↓
matplotlib plot
```

Example CSV format (`test_data.csv`):

```
timestamp,x,y,z
0.001,0.02,0.01,0.05
0.002,0.03,0.01,0.06
```

See [communication.md](communication.md) for the serial protocol details
and the corresponding read script.
