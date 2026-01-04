Rocket Launch & Telemetry Simulation

A physics-based rocket launch simulation written in Python and developed incrementally in clearly defined phases.
The project focuses on Newtonian mechanics, time-stepped simulation, and clean software design.

The simulation is CLI-based and prioritizes correctness and clarity over visual polish.
```
## ▶ How to Run

**Requirements:**
- Python 3.10+

**Run the simulation:**
```bash
python3 main.py
```
The simulation will print live telemetry to the terminal and exit once the success condition is met.

📁 Project Structure
```
rocket_sim/
├── main.py      # Simulation loop, time tracking, telemetry output
├── rocket.py    # Rocket state and physics calculations
├── README.md
└── .gitignore
```

📌 Project Status

Phase 1: ✅ Complete

Phase 2: ✅ Complete

Phase 3: ✅ Complete

Phase 4: 🔜 Planned

---

✅ Phase 1 — Simulation Foundation (Completed)

Goal:
Establish a working simulation loop that produces visible, stable output.

Implemented:

Time-stepped update loop (dt)

Rocket state tracking (altitude, velocity)

Single-line telemetry output

Basic success condition based on altitude

Outcome:
A functioning program that simulates a simple ascent and validates the overall structure.

---

✅ Phase 2 — Physics-Based Vertical Ascent (Completed)

Goal:
Simulate a realistic vertical rocket ascent using Newtonian physics.

Implemented:

Thrust-based acceleration model:
```
a = (thrust / mass) - g
```

Constant gravity model (g = 9.81 m/s²)

Falcon 9–inspired constants:

Mass: 549,000 kg

Thrust: 7,607,000 N

Smooth integration of: Acceleration → Velocity → Altitude

Clear separation of responsibilities:

Rocket owns physics and state

main owns time, loop, and output

Telemetry output includes:
```
| Time: 00:02:08.30s | Velocity: 1827.96 m/s | Altitude: 80057.48 m
| Acceleration: 35.45 m/s^2 | Mass: 168071.60 kg | Thrust 7607000 N |
```

Success Condition:

Rocket reaches target “space” altitude

Mission success message printed

Outcome:
A physically believable vertical ascent simulation with correct force modeling.

---

🚀 Current Features (Phase 3)
🧩 Architecture

Rocket

Owns motion state: velocity, altitude, acceleration

Aggregates one or more Stage objects

Computes net force, acceleration, and kinematics

Stage

Owns physical properties:

dry_mass

fuel_mass

thrust

burn_rate

Computes its own total mass

Can be activated/deactivated dynamically

This follows composition over inheritance and clean separation of responsibility.

🔥 Physics Model

Constant thrust per active stage

Fuel mass decreases over time based on burn_rate × dt

Rocket mass is computed dynamically from attached stages

Acceleration calculated using:
```
F_net = thrust − weight
a = F_net / total_mass
```

Gravity fixed at 9.81 m/s²

Simple G-limit logic:

Stage deactivates when acceleration exceeds 35 m/s²

---

🌍 Phase 4 — Orbital Mechanics (Planned)

Goal:
Transition from altitude-based success to orbit-based success.

Planned Features:

Orbital velocity thresholds (e.g., LEO)

Success based on:

Altitude and

Orbital velocity

Separation of ascent and orbital logic

Foundation for multi-stage rockets

---

🚫 Current Non-Goals

The following are intentionally out of scope for now:

Atmospheric drag

Staging

Multi-axis motion

Guidance or control systems

Graphical visualization

***

🧠 Design Philosophy

Build one correct layer at a time

Avoid premature abstraction

Prioritize clarity over complexity

Physics before features

***

