# Rocket Launch & Telemetry Simulation

Physics-based multi-stage rocket simulation in Python.  
Focuses on Newtonian mechanics, staging, guidance, and telemetry — not graphics.

Models a Falcon 9–class vehicle through ascent to near-orbital conditions.  
**Full orbital insertion / circularization is not implemented yet.**

---

## Features

- Multi-stage vehicle with per-stage fuel and mass
- State-machine flight phases (launch → pitch kick → ascent → staging → stage 2 → coast)
- Configurable guidance (pitch initiation, stage 1 & 2 pitch programs)
- Thrust, gravity, and atmospheric drag
- Fairing jettison
- Live console telemetry
- CSV telemetry logging (timestamped files under `telemetry_data/`)
- Fast mode for quicker test runs

---

## Project Layout

```text
src/rocket_sim/
├── cli.py              # Entry point / simulation loop
├── utils.py            # CLI helpers (time string, --fast flag)
├── config/             # Dataclasses + Falcon 9 vehicle data
├── models/             # Rocket, Stage
├── guidance/           # Pitch initiation, stage 1 & 2 guidance
├── physics/            # Forces and motion helpers
└── telemetry/          # Console formatter + CSV recorder
```

- Vehicle numbers live in `config/` (especially `config/falcon9_config.py`).
- Guidance logic lives under `guidance/`. 
- The rocket state machine orchestrates the flight phases.

---

## Requirements

- **Python 3.10+**
- `uv` recommended (or standard `pip`)

---

## Setup

```bash
git clone https://github.com/RobM-Tech/Rocket-Simulation.git
cd Rocket-Simulation

uv venv
source .venv/bin/activate          # On Windows use: .venv\Scripts\activate
uv pip install -e .
```

---

## Run

From the project root, with your virtual environment active:

```bash
python -m rocket_sim.cli
```

### Fast Mode
Skips the per-step sleep interval so the simulation finishes in seconds instead of several minutes. Telemetry still prints to the console and data still logs to the CSV file. This is highly useful while developing and testing.

```bash
python -m rocket_sim.cli --fast
```

*or with uv:*

```bash
uv run -m rocket_sim.cli --fast
```

Without the `--fast` flag, the loop sleeps during each step so that the readout mirrors the simulation timestep (dt), making it watchable in roughly real time.

---

## Telemetry CSV

During a simulation run, telemetry data is appended every 100 steps (and once more at the conclusion of the run) to a timestamped file:

```text
telemetry_data/telemetry_YYYYMMDD_HHMMSS.csv
```

The directory is created automatically if it is missing. These generated CSV files are ignored by git.

---

## Configuration

Edit `src/rocket_sim/config/falcon9_config.py` to tune parameters such as:

- Stage masses, thrust, and burn rate
- Pitch schedules and staging thresholds
- Payload, fairing, and reference aerodynamic areas

*Note: Guidance angles in the configuration file are set in degrees; conversion to radians happens automatically inside the guidance functions.*

---

## Current Limits

- Reaches roughly orbital horizontal speed at high altitude, but does not model a stable circular orbit.
- No orbital insertion or coast-orbit physics yet.
- No automated test suite yet.

---

## Status

The package layout, config-driven vehicle modules, extracted guidance logic, console + CSV telemetry formatting, and CLI `--fast` mode are all successfully in place.

**Next focus:** Writing a comprehensive automated unit test suite (`pytest`) covering the guidance formulas and core vehicle models.
