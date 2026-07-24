"""
hu108_test.py

Phase-1 (no ROS) test pipeline for the HU108 vibration sensor:

    HU108 -> serial -> parse -> CSV -> matplotlib plot

Two modes:
  --simulate   use mock_serial.MockHU108Serial (no hardware needed)
  (default)    use a real serial.Serial connection (needs pyserial +
               an actual HU108 plugged in)

Usage:
  python3 hu108_test.py --simulate --duration 10
  python3 hu108_test.py --port /dev/ttyUSB0 --baud 115200 --duration 10
"""

import argparse
import csv
import time

import matplotlib
matplotlib.use("Agg")  # safe default for headless testing; drop this line
                        # for a live-updating window on your own machine
import matplotlib.pyplot as plt


def open_source(args):
    if args.simulate:
        from mock_serial import MockHU108Serial
        print("[info] running in --simulate mode (no hardware required)")
        return MockHU108Serial()
    else:
        import serial
        print(f"[info] opening real serial port {args.port} @ {args.baud}")
        return serial.Serial(args.port, args.baud, timeout=1)


def parse_line(raw_line):
    """
    Parse one line of sensor output into (x, y, z).
    Replace this once the *real* HU108 frame format is confirmed -
    this assumes a simple 'x,y,z' text line, which matches the mock
    source and is a reasonable first guess, but the real sensor may
    use a binary frame instead (see hardware/HU108/communication.md).
    """
    line = raw_line.decode(errors="ignore").strip()
    if not line:
        return None
    try:
        x, y, z = map(float, line.split(","))
    except ValueError:
        return None
    return x, y, z


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--simulate", action="store_true",
                         help="use synthetic data instead of real hardware")
    parser.add_argument("--port", default="/dev/ttyUSB0",
                         help="serial port (real mode only)")
    parser.add_argument("--baud", type=int, default=115200,
                         help="baud rate (real mode only)")
    parser.add_argument("--duration", type=float, default=10.0,
                         help="how many seconds to record")
    parser.add_argument("--csv-out", default="test_data.csv")
    parser.add_argument("--plot-out", default="test_data.png")
    args = parser.parse_args()

    source = open_source(args)

    timestamps, xs, ys, zs = [], [], [], []
    start = time.time()

    with open(args.csv_out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "x", "y", "z"])

        while time.time() - start < args.duration:
            raw_line = source.readline()
            parsed = parse_line(raw_line)
            if parsed is None:
                continue
            x, y, z = parsed
            t = time.time() - start

            writer.writerow([f"{t:.4f}", x, y, z])
            timestamps.append(t)
            xs.append(x)
            ys.append(y)
            zs.append(z)

    source.close()
    print(f"[info] recorded {len(timestamps)} samples over "
          f"{args.duration:.1f}s -> {args.csv_out}")

    # Plot
    plt.figure(figsize=(10, 4))
    plt.plot(timestamps, xs, label="X")
    plt.plot(timestamps, ys, label="Y")
    plt.plot(timestamps, zs, label="Z")
    plt.xlabel("time (s)")
    plt.ylabel("vibration amplitude")
    plt.title("HU108 vibration test" + (" (simulated)" if args.simulate else ""))
    plt.legend()
    plt.tight_layout()
    plt.savefig(args.plot_out, dpi=120)
    print(f"[info] plot saved -> {args.plot_out}")

    # For live testing on your own machine (not headless), you can instead
    # call plt.show() to pop up an interactive window.


if __name__ == "__main__":
    main()
