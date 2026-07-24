# HU108 Test Pipeline — Logic & Verification Guide
# HU108 测试流程 —— 逻辑与验证说明

---

## 1. Two Different Questions / 两个不同的问题

There are two completely different questions that are easy to confuse:
这里有两个很容易混淆的问题，需要先分清楚：

| Question / 问题 | Answered by / 靠什么回答 |
|---|---|
| **Does my code work?**<br>我的代码能不能正常运行？ | Simulated test (`--simulate`)<br>模拟数据测试 |
| **Is my sensor / vibration data good?**<br>我的传感器 / 振动数据好不好？ | Real hardware test<br>真实硬件测试 |

The `--simulate` mode **only answers the first question**. The data it
produces is synthetic (made up by `mock_serial.py`), so asking "is this
data good or bad" does not make sense yet — there is no real physical
phenomenon behind it.

`--simulate` 模式**只回答第一个问题**。它产生的数据是编造出来的
（在 `mock_serial.py` 里手写的），所以问"这个数据好不好"目前是没有意义的——
它背后没有真实的物理现象。

---

## 2. What `mock_serial.py` Actually Generates
## `mock_serial.py` 到底生成了什么

```python
x = 0.05 * sin(2π * 3.0 Hz * t) + noise
y = 0.03 * sin(2π * 5.0 Hz * t) + noise
z = 0.02 * sin(2π * 1.5 Hz * t) + noise
# plus a brief "spike" roughly every 5 seconds
# 另外每隔约5秒加一个"冲击"尖峰
```

This is a **known, designed signal** — I chose these frequencies and
amplitudes myself. The purpose is to have a signal with a *known ground
truth*, so we can check whether the pipeline correctly captures and
reproduces it.

这是一个**已知的、人为设计的信号**——频率和振幅是我自己定的。
目的是让这个信号有一个"已知的标准答案"，这样才能检查整条流程有没有正确地
把它采集、解析、画出来。

---

## 3. What This Test Actually Verifies (Software Pipeline)
## 这次测试真正验证的内容（软件流程）

| Check / 检查项 | How to verify / 怎么验证 | What it tells you / 说明了什么 |
|---|---|---|
| Sampling is steady, no major stalls<br>采样是否稳定、没有明显卡顿 | Look at the `timestamp` column in the CSV — intervals should be close to the designed rate (~0.01s / 100Hz)<br>看 CSV 的 timestamp 列，间隔应接近设计值(约0.01秒/100Hz) | Whether the read loop has bugs (blocking, dropped reads)<br>读取循环有没有问题（阻塞、丢帧） |
| Plot matches the designed signal<br>画出的波形是否符合设计 | X should oscillate faster than Z (3Hz vs 1.5Hz); Y fastest of all (5Hz)<br>X轴应该比Z轴跳动快(3Hz vs 1.5Hz)；Y轴最快(5Hz) | Whether `parse_line()` correctly maps columns to X/Y/Z (order not swapped)<br>解析函数有没有把x,y,z的顺序搞混 |
| Spike appears where expected<br>尖峰出现在预期位置 | A visible jump near t≈0s (and every ~5s for longer runs)<br>在 t≈0秒附近（以及每隔约5秒）应该有明显跳变 | Whether transient/anomaly events are captured, not smoothed away<br>瞬态/异常事件有没有被正确捕捉,而不是被平滑掉了 |
| Row count matches expected duration<br>数据行数是否符合预期时长 | ~duration × 100 rows (e.g. 3s → ~300 rows)<br>约 时长×100 行（例如3秒 → 约300行） | Whether samples are being silently dropped<br>有没有静默丢数据 |

### Example check we already ran / 已经跑过的示例检查

```
样本数 (samples): 298
时间跨度 (duration): 3.009 秒 (s)
平均采样间隔 (avg interval): 0.0101 秒 (s)  — designed value / 设计值: 0.01s
```

This matched the design closely, confirming the pipeline logic (read →
parse → CSV → plot) works correctly.

这个结果和设计值几乎一致，说明整条流程（读取→解析→存CSV→画图）的逻辑没有问题。

---

## 4. What "Good Data" Means Once Real Hardware Is Connected
## 接上真实硬件之后，"数据好不好"应该怎么判断

Once the HU108 is physically connected, the checks change from "does the
code work" to "is the sensor behaving correctly / is the signal
trustworthy":

一旦接上真实的 HU108，检查的重点就从"代码对不对"变成"传感器表现是否正常 / 信号是否可信"：

### 4.1 Noise floor at rest / 静止状态下的噪声水平
- Leave the sensor stationary on a table.
- 把传感器静置在桌面上不动。
- Readings should hover close to 0, with only small random noise.
- 读数应接近0，只有很小的随机噪声。
- **Bad sign / 异常信号**: large swings (e.g. ±0.5) while completely still →
  wiring issue, grounding problem, or sensor fault.
- **异常表现**：完全静止时读数却大幅跳动（比如 ±0.5）→ 可能是接线问题、
  接地问题，或传感器本身故障。

### 4.2 Response to a known excitation / 对已知激励的响应
- Gently tap the surface the sensor is mounted on.
- 轻敲传感器所在的表面。
- You should see a clear spike, followed by decay back to baseline.
- 应该能看到明显的尖峰，然后衰减回基线水平。
- **Bad sign / 异常信号**: no reaction to a tap, or the signal keeps
  oscillating/diverging instead of settling → sampling or filtering issue.
- **异常表现**：敲击没有反应，或者信号持续震荡/发散而不收敛 →
  可能是采样或滤波方面的问题。

### 4.3 Axis independence / 三轴是否独立
- Move/shake the sensor along one axis only (e.g. X).
- 只沿一个方向（比如X轴）晃动传感器。
- Mainly the corresponding axis should show large changes; the others
  should stay relatively calm.
- 主要应该是对应那个轴的读数变化大，其他轴应相对平稳。
- **Bad sign / 异常信号**: all three axes always move together → possible
  mounting orientation issue or a bug in the acquisition code.
- **异常表现**：三个轴总是同步一起变化 → 可能是安装方向问题，
  或采集代码有bug。

### 4.4 Sampling stability / 采样稳定性
- Same check as in the simulated test — inspect timestamp intervals in
  the CSV for consistency.
- 和模拟测试一样的检查方法——看CSV里的timestamp间隔是否一致。

### 4.5 Compare against the datasheet / 对照数据手册
- Measurement range, resolution, and noise density from the vendor
  datasheet should roughly bound what you observe.
- 厂商数据手册里的量程、分辨率、噪声密度，应该能大致框住你实测出来的数值范围。
- This is why `hardware/HU108/datasheet.md` has `TBD` fields to fill in
  once the real spec is confirmed.
- 这也是为什么 `hardware/HU108/datasheet.md` 里留了 `TBD` 字段，
  等确认了真实参数之后再填上。

---

## 5. Summary / 总结

| Stage / 阶段 | Data source / 数据来源 | Question answered / 回答的问题 |
|---|---|---|
| `--simulate` | Synthetic, designed by us<br>人为设计的合成数据 | Does the pipeline (code) work correctly?<br>整条流程（代码）是否正常运行？ |
| Real hardware<br>真实硬件 | Actual HU108 output<br>真实的HU108输出 | Is the sensor / signal trustworthy?<br>传感器/信号是否可信？ |

Don't judge sensor quality from simulated data, and don't judge code
correctness only by "it produced some numbers" — check the specific
signs above for each stage.

不要用模拟数据去判断传感器好坏，也不要仅凭"跑出了一些数字"就认为代码没问题——
针对每个阶段，按上面列的具体检查项逐一确认。
