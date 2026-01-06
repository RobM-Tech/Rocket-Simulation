Rocket Launch & Telemetry Simulation

A physics-based rocket launch simulation in Python, designed incrementally with a focus on Newtonian mechanics, multi-stage rockets, and clean software design. The simulation is CLI-based, prioritizing accuracy, telemetry clarity, and modular architecture over graphical polish.

▶ Features (Current State)

---

Multi-Stage Rocket Simulation

The Rocket class aggregates one or more Stage objects.

Each Stage has:

dry_mass, fuel_mass, thrust, burn_rate

Lifecycle states: CREATED, ATTACHED, IGNITED, BURNED_OUT, SEPARATED

Handles its own fuel consumption and mass updates

The rocket controls stage states, including ignition, MECO, and separation, via a state machine.

---

Physics & Motion

Time-stepped simulation (dt) updates velocity and altitude each tick.

Net force & acceleration calculated dynamically:

F_net = thrust − weight

a = F_net / total_mass

Gravity fixed at 9.81 m/s².

G-limit logic: a stage automatically deactivates if acceleration exceeds 35 m/s².

---

Telemetry

Live, terminal-friendly telemetry:
```
Time | Velocity | Altitude | Acceleration | Mass | Thrust | Stage States
```

Updates in place to avoid clutter.

Shows Rocket state, Current stage, and Next stage.

---

Multi-Stage Flight

Stage separation triggered at target conditions (altitude, velocity).

current_stage and next_stage tracking ensures smooth stage handoff.

Rocket mass dynamically recalculated from all attached stages.

Supports ignition delays between stages without blocking simulation ticks.

---

▶ How to Run

Requirements:

Python 3.10+

Run the simulation:
```
python3 main.py
```
---

Telemetry prints live in the terminal.

Simulation exits when mission success is reached.

📁 Project Structure
```
rocket_sim/
├── main.py      # Simulation loop, time tracking, telemetry output
├── rocket.py    # Rocket class, physics, stage controller
├── stage.py     # Stage class, fuel, states, helpers
├── README.md
└── .gitignore
```

---

🚀 Current Phases
Phase 1 — Simulation Foundation ✅

Time-stepped loop

Rocket state tracking

Single-line telemetry output

Basic success condition based on altitude

---

Phase 2 — Physics-Based Vertical Ascent ✅

Newtonian motion for velocity & altitude

Thrust and mass dynamically modeled

Smooth integration: acceleration → velocity → altitude

Telemetry includes velocity, altitude, acceleration, mass, thrust

---

Phase 3 — Multi-Stage & Composition ✅

Introduced Stage objects with separate mass and burn logic

Rocket aggregates stages and computes total mass

Stage lifecycle states (IGNITED, BURNED_OUT, SEPARATED)

Stage separation logic implemented

Telemetry now shows current and next stage states

State machine drives the rocket’s progression

---

Phase 4 — Orbital Mechanics & State Machine 🔜

Rocket driven by a state machine

Planned: orbital velocity thresholds, more advanced mission success

Foundation for multi-stage orbital flight

Non-blocking stage ignition delays

---

🧠 Design Philosophy

Build one correct layer at a time

Avoid premature abstraction

Prioritize clarity over complexity

Physics before features, states before automation

