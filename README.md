# 🚀 Rocket Simulator — Phase 1 (Proof of Life)

## Project Overview

This project is a **simple rocket launch simulation written in Python**. Phase 1 focuses on proving that a time-stepped physics simulation works by showing a rocket moving upward under constant thrust and gravity.

This phase is intentionally minimal. The goal is **not realism**, but correctness, clarity, and a working foundation for future phases.

---

## 🎯 Phase 1 Goal

> Build the smallest possible program that simulates vertical motion over time and prints live telemetry to the terminal.

If the rocket moves and the numbers make sense, Phase 1 is a success.

---

## ✅ Features Included (Phase 1 Scope)

* Vertical-only motion
* Constant thrust
* Constant mass
* Constant gravity (9.81 m/s²)
* Fixed time step simulation loop
* Terminal telemetry output

---

## 🚫 Features Explicitly Excluded

The following are **not allowed in Phase 1** and are reserved for later phases:

* Fuel or burn rate
* Changing mass
* Drag or atmosphere
* Angled launches
* Staging
* File output
* Graphs or visualization
* GUI or animation

---

## 🧠 Physics Model (Simplified)

The simulation uses Newton's Second Law:

```
F = m * a
```

Where:

* Thrust provides upward force
* Gravity provides constant downward acceleration

Acceleration is calculated as:

```
a = (thrust / mass) - gravity
```

Velocity and altitude are updated incrementally each time step.

---

## 📊 Telemetry Output

At each time step, the program prints:

* Time (seconds)
* Altitude (meters)
* Velocity (m/s)

Example output:

```
Time: 2.5s | Altitude: 84.3m | Velocity: 38.7m/s
```

---

## 🧱 Project Structure (Phase 1)

```
rocket_sim/
├── main.py   # Contains rocket class and simulation loop
└── README.md
```

---

## ▶️ How to Run

1. Ensure Python 3.10+ is installed
2. Navigate to the project directory
3. Run:

```
python main.py
```

---

## 📌 Phase 1 Completion Criteria

Phase 1 is considered complete when:

* The program runs without errors
* The rocket altitude changes over time
* Telemetry prints every time step
* The physics behavior can be explained

Once complete, development moves to **Phase 2: Fuel, Mass Change, and Data Logging**.

---

## 🛠 Future Phases (High-Level)

* **Phase 2:** Fuel burn, mass change, apogee, telemetry logging
* **Phase 3:** Visualization, plotting, configuration, analysis

---

## Author Notes

This project is designed as a learning-focused simulation emphasizing clarity, incremental development, and engineering discipline.
