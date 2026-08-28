# Rocket Launch & Telemetry Simulation

A physics-based, multi-stage rocket simulation written in Python. 

This project focuses on correct Newtonian mechanics, staging, guidance, and clear telemetry rather than fancy graphics. The simulation models a Falcon 9-class vehicle up to near-orbital conditions. 

*Note: Full orbital insertion is not implemented yet.*

---

## Current Status (v1.1.0)

The project is currently being reworked into a proper package structure:

```text
src/rocket_sim/
├── models/       # Rocket + Stage
├── physics/
├── guidance/
├── telemetry/
└── config/
```

> ⚠️ **In Progress:** Some files have been moved to the new structure, while others are still located at the root directory.

---

## How to Run

Execute the simulation from the project root (with your virtual environment active):

```bash
python main.py
```

*Live telemetry will print directly to the terminal.*

---

## What’s Modeled

* **Multi-stage vehicle:** Independent fuel tracking and mass properties per stage.
* **State-machine flight phases:** Automated sequencing from liftoff to staging.
* **Pitch guidance:** Initial gravity turn kick followed by programmatic ramps.
* **Environmental physics:** Dynamic thrust, gravity losses, and atmospheric drag.
* **Fairing jettison:** Aerodynamic shield deployment based on altitude.
* **Live telemetry:** Real-time data streams for kinematics, aero, propulsion, and flight state.

---

## Known Limits

* Reaches ~290 km altitude but cannot yet achieve full orbital velocity.
* No circularization logic or advanced orbital mechanics implemented yet.
