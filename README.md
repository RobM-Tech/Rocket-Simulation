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

Smooth integration of:

Acceleration → Velocity → Altitude

Clear separation of responsibilities:

Rocket owns physics and state

main owns time, loop, and output

Telemetry output includes:

-Time

-Velocity

-Altitude

-Acceleration

-Mass

-Thrust

Success Condition:

Rocket reaches target “space” altitude

Mission success message printed

Outcome:
A physically believable vertical ascent simulation with correct force modeling.

---

🧭 Phase 3 — Fuel Burn & Variable Mass (Planned)

Goal:
Introduce mass change over time and increasing acceleration.

Planned Features:

Fuel mass and burn rate

Decreasing total mass per timestep

Increasing acceleration as mass drops

Engine cutoff when fuel is depleted

Expanded success and failure states

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

📌 Project Status

Phase 1: ✅ Complete

Phase 2: ✅ Complete

Phase 3: 🔜 Planned

Phase 4: 🔜 Planned