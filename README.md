# Rocket Launch & Telemetry Simulation
![CI](https://github.com/RobM-Tech/Rocket-Simulation/actions/workflows/tests.yaml/badge.svg)

Physics-based multi-stage rocket simulation in Python.

Focuses on Newtonian mechanics, staging, guidance, and telemetry — not graphics.

Models a Falcon 9–class vehicle through ascent to near-orbital conditions.

**Full orbital insertion / circularization is not implemented yet.**

**Version 1.3.0** — packaged layout, configuration-driven vehicle parameters, extracted flight profile boundaries, console + CSV telemetry, CLI fast mode, and stateless kinematics unit testing.


---

## What this project demonstrates

- Separation of **vehicle data** (config), **guidance laws** (pure functions), and **flight sequencing** (state machine on the rocket)
- Multi-stage mass/fuel accounting and fairing jettison
- Testable pitch guidance without running a full ascent
- Practical operator tooling: live telemetry, CSV export, `--fast` runs
- Stateless Physics & Kinematics Engine


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
- Unit tests for pitch initiation
- Unit tests for guidance and stage mass/fuel behavior
- CI via GitHub Actions (pytest on push to `main`)
- Script to plot altitude vs time from the latest telemetry CSV
- CLI run modes: `--fast` and `--until MECO|SECO|FULL` for partial or full flights
- Telemetry CSV and plots organized by run phase (`telemetry_data/data_MECO`, `docs/plot_MECO`, etc.)
- Aerodynamic dynamic pressure ($Q$) tracking with real-time Max-Q peak structural load monitoring.
- Clamped barometric altitudinal scaling to safely prevent mathematical domain errors at deep space boundaries ($150\text{ km}+$).
- Transonic wave-drag coefficient ($C_d$) spikes approximating the breaking of the sound barrier (Mach $0.8$ to Mach $1.2$).


---

## Project layout

```text
src/rocket_sim/
├── cli.py         # Entry point / simulation loop
├── utils.py       # CLI helpers (time string, --fast flag)
├── config/        # Dataclasses + Falcon 9 vehicle data
├── models/        # Rocket, Stage models & state machine
├── guidance/      # Pitch initiation, stage 1 & 2 guidance
├── physics/       # Stateless forces and kinematics engine
└── telemetry/     # Console telemetry formatter + CSV recorder


tests/
└── unit/          # Guidance unit tests
```

- Vehicle numbers live in `config/` (especially `falcon9_config.py`).
- Guidance logic lives under `guidance/`.
- The rocket state machine orchestrates flight phases.

### Design notes

| Concern | Where it lives |
| :--- | :--- |
| Masses, thrusts, pitch schedules (degrees) | `config/` + Falcon 9 data module |
| Pitch programs (pure functions) | `guidance/` |
| Flight phase sequencing, staging | `models/rocket.py` state machine |
| Forces / kinematics helpers | `physics/` |
| Presenting and logging telemetry | `telemetry/` |

- Guidance config values are in degrees; conversion to radians happens inside guidance functions.
- Runtime state (fuel remaining, current pitch, flags) lives on Rocket / Stage, not in config objects.

---

## Requirements

- Python 3.10+
- `uv` recommended (or `pip`)

---

## Setup

```bash
git clone https://github.com/RobM-Tech/Rocket-Simulation.git
cd Rocket-Simulation
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -e .
```

### Development install (tests)

```bash
uv pip install -e ".[dev]"
```

This pulls optional dev dependencies (including `pytest`). Runtime simulation does not require `pytest`.

---

## Run

From the project root, with the virtual environment active:

```bash
python -m rocket_sim.cli
```

### Fast mode

Skips per-step sleep so a run finishes in seconds instead of several minutes. Console telemetry and CSV logging still run.

```bash
python -m rocket_sim.cli --fast
```

or:

```bash
uv run -m rocket_sim.cli --fast
```

Without `--fast`, the loop sleeps each step so the readout is watchable in roughly real time.

### Stop at a phase

End the run at a defined flight phase (useful for debugging and shorter CSVs):

```bash
python -m rocket_sim.cli --until MECO
python -m rocket_sim.cli --fast --until SECO
```
| Value | Behavior |
| :--- | :--- |
| **FULL** | runs until orbit coast. There is no closed-orbit propagation yet, so the simulation ends there by design. |
| **MECO** | Stop at main-engine cutoff / stage 1 MECO |
| **SECO** | Stop at second-engine cutoff |
---

## Tests

```bash
uv pip install -e ".[dev]"  # if not already installed
pytest
```

or:

```bash
uv run pytest
```

Unit tests cover pitch initiation and stage 1 / stage 2 guidance (branch selection, rate limiting, throttle bias) without a full mission run.

The same suite runs in CI on every push to `main` (see the **Actions** tab).

---

## Telemetry CSV

During a run, telemetry is appended every 100 steps (and once at the end) to a timestamped file:

The directory is created if missing. Generated CSV files are gitignored.
CSVs are written under a phase folder based on `--until`:

```text
telemetry_data/data_MECO/
telemetry_data/data_SECO/
telemetry_data/data_FULL/
```

---

## Sample output

After a run, CSVs land in `telemetry_data/`. You can generate a quick altitude history plot:

```bash
python scripts/plot_run.py
```
Plots from a run are saved under `docs/plot_MECO` (or `plot_SECO` / `plot_FULL`) to match the phase flag.
Output folders for logs and plots follow the same phase tag so MECO/SECO/FULL runs stay separated.

Flight data from a logged CSV run:
-Climb profile
-Energy build-up
-Trajectory shape

 **Flight Analysis Profile:** The telemetry plots distinctly show a flattening velocity curve mid-ascent (between 60s and 80s). This accurately reflects the vehicle throttling down to mitigate structural stress while passing through maximum aerodynamic pressure (Max-Q).
![Altitude vs mission time](docs/flight_data_telemetry_sample.png)

## Configuration

Edit `src/rocket_sim/config/falcon9_config.py` to tune:
- Stage masses, thrust, burn rate
- Pitch schedules and staging thresholds
- Payload / fairing / reference area

---

## Current limits

- Reaches roughly orbital horizontal speed at high altitude, but does not model a circular orbit
- No orbital insertion or closed-orbit propagation yet
- Throttling schedules are completely abstracted out of core execution files into configuration dataclass components. Telemetry loop decoupling remains ongoing.

---