"""
mock_serial.py

A fake "serial port" that mimics the small part of pyserial's interface
used by hu108_test.py (readline()), so the rest of the pipeline
(parsing -> CSV -> plotting) can be tested without any real hardware.

It generates a synthetic 3-axis vibration signal:
- baseline sine waves on X/Y/Z at different frequencies
- small random noise
- occasional "spike" every ~5 seconds to mimic an anomaly/impact event

Once real hardware is available, this file is not imported at all -
hu108_test.py falls back to the real `serial.Serial` class instead.
"""

import math
import random
import time


class MockHU108Serial:
    def __init__(self, port=None, baudrate=None, timeout=1):
        # port/baudrate accepted for interface-compatibility with
        # serial.Serial(port, baudrate, timeout=...), but unused here.
        self._start = time.time()
        self._sample_interval = 0.01  # simulate ~100 Hz output
        self._last_emit = 0.0

    def readline(self):
        # Pace output to roughly match a real sensor's sample rate.
        now = time.time()
        elapsed = now - self._start
        sleep_for = self._sample_interval - (now - self._last_emit)
        if sleep_for > 0:
            time.sleep(sleep_for)
        self._last_emit = time.time()

        t = self._last_emit - self._start

        x = 0.05 * math.sin(2 * math.pi * 3.0 * t) + random.uniform(-0.005, 0.005)
        y = 0.03 * math.sin(2 * math.pi * 5.0 * t) + random.uniform(-0.005, 0.005)
        z = 0.02 * math.sin(2 * math.pi * 1.5 * t) + random.uniform(-0.005, 0.005)

        # Inject a brief "spike" every ~5 seconds to mimic an impact/anomaly.
        if int(t) % 5 == 0 and (t - int(t)) < 0.05:
            x += 0.3
            y += 0.15

        line = f"{x:.4f},{y:.4f},{z:.4f}\n"
        return line.encode("utf-8")

    def close(self):
        pass
