# Rocket Launch & Telemetry Simulation

# Rocket Launch & Telemetry Simulation

Physics-based multi-stage rocket simulation in Python. Focuses on Newtonian mechanics, staging, guidance, and telemetry — not graphics. Models a Falcon 9–class vehicle through ascent to near-orbital conditions. 

**Full orbital insertion / circularization is not implemented yet.**

---

## Features

- **Multi-stage vehicle** with per-stage fuel and mass tracking.
- **State-machine flight phases** (launch → pitch kick → ascent → staging → stage 2 → coast).
- **Configurable guidance** (pitch initiation, stage 1 & 2 pitch programs).
- **Atmospheric physics** modeling thrust, gravity, and atmospheric drag.
- **Fairing jettison** implementation.
- **Live console telemetry** tracking kinematics, aero, propulsion, and flight state.

---

## Project Layout

```text
src/rocket_sim/
├── cli.py            # Entry point / simulation loop
├── config/           # Dataclasses + Falcon 9 vehicle data
├── models/           # Rocket, Stage
├── guidance/         # Pitch initiation, stage 1 & 2 guidance
├── physics/          # Forces and motion helpers
└── telemetry/        # Console formatter (data dict → text)
```

- **Vehicle numbers** live in `config/` (especially `config/falcon9_config.py`).
- **Guidance logic** lives under `guidance/`.
- **The rocket state machine** orchestrates the different flight phases.

---

## Requirements

- **Python 3.10+**
- [uv](https://github.com/astral-sh/uv) recommended (or standard `pip`)

---

## Setup

```bash
git clone https://github.com/RobM-Tech/Rocket-Simulation.git
cd Rocket-Simulation
uv venv
source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
uv pip install -e .
```

---

## Running the Simulation

From the project root, with your virtual environment active, run either command:

```bash
python -m rocket_sim.cli
```

*or*

```bash
python src/rocket_sim/cli.py
```

> **Note:** Live telemetry prints directly to the terminal. A full ascent can take several minutes of real time because the simulation loop mirrors the simulation timestep (`dt`) with a sleep interval to provide a watchable readout.

---

## Configuration

Edit `src/rocket_sim/config/falcon9_config.py** to tune parameters such as:
- Stage masses, thrust, and burn rate.
- Pitch schedules and staging thresholds.
- Payload, fairing, and reference aerodynamic areas.

*Note: Guidance angles in the configuration file are set in degrees; conversion to radians happens automatically inside the guidance functions.*

---

## Current Limits

- **No circular orbit modeling:** Reaches roughly orbital horizontal speed at high altitude, but does not transition into a stable circular orbit.
- **No orbital insertion:** Coast-orbit physics are not yet implemented.
- **Console-only telemetry:** Data outputs only to the terminal (CSV export is planned).
- **No test suite:** Automated unit tests are not yet implemented.

---

## Current Status & Next Steps

The structural refactor is complete, including the package layout, config-driven vehicle modules, extracted guidance logic, and a telemetry split between data processing and console formatting. 

Future development is focused on:
- Implementing faster, headless simulation runs.
- Adding CSV telemetry logging.
- Writing a comprehensive automated unit test suite.