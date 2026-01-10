Rocket Launch & Telemetry Simulation

A physics-based rocket launch simulation in Python, built incrementally with a strong focus on Newtonian mechanics, multi-stage flight, guidance logic, and clean system design.
The simulation is CLI-based, prioritizing telemetry clarity, correctness, and modular architecture over graphics.

This project intentionally models real launch behavior up to near-orbital conditions, while clearly documenting the limits of the current physics model.

---

Why this project exist:

This project exists to build a realistic, physics-driven rocket simulation from first principles.

Instead of hard-coded trajectories or visual shortcuts, the simulation models mass flow, thrust vectoring, multi-stage separation, and guidance logic using Newtonian mechanics and a state machine. Every behavior is traceable through live telemetry, making the system debuggable and extensible.

The project currently stops short of full orbital mechanics to expose why orbital insertion is difficult—highlighting the importance of horizontal velocity, pitch timing, and gravity losses—with orbital dynamics planned as the next phase

---

▶ How to Run
Requirements

Python 3.10+

```
Run the simulation
python3 main.py
```

Telemetry prints live in the terminal.

```
📁 Project Structure
rocket_sim/
├── main.py      # Simulation loop, time tracking, telemetry output
├── rocket.py    # Rocket class, state machine, guidance logic
├── physics.py   # Forces, drag, thrust vectoring
├── stage.py     # Stage class, fuel, mass, lifecycle states
├── README.md
└── .gitignore
```
---

Multi-Stage Rocket Simulation

The Rocket class aggregates one or more Stage objects.

Each Stage has:

dry_mass, fuel_mass, thrust, burn_rate

Lifecycle states:

    --CREATED

    --ATTACHED

    --IGNITED

    --BURNED_OUT

    --SEPARATED

Each stage:

Manages its own fuel consumption

Computes its own remaining mass

The rocket controls:

Ignition

MECO

Stage separation

Stage handoff
via a state machine, not ad-hoc conditionals.

---

Physics & Motion

Time-stepped simulation (dt) updates motion each tick.

Separate vertical and horizontal kinematics:

Velocity and acceleration tracked independently in X and Y.

Forces modeled:

Thrust (split by pitch angle)

Gravity (constant 9.81 m/s²)

Atmospheric drag (exponential density model)

Acceleration computed dynamically:
```
a = F_net / total_mass
```

G-limit protection:

A stage automatically deactivates if acceleration exceeds 35 m/s².

---

Guidance, Pitch & Flight Profile

This simulation now includes explicit pitch guidance, not just vertical ascent.

Pitch System Overview

Pitch is stored internally in radians

Thrust is split into horizontal and vertical components:

T_x = T * sin(pitch)
T_y = T * cos(pitch)

Flight Phases with Guidance

The rocket is driven by a state machine, including:

    --LAUNCH

    --PITCH_INITIATION

    --ASCENT_BURN

    --STAGE1_SEPARATION

    --COAST

    --STAGE2_IGNITION

    --STAGE2_ASCENT

Pitch Initiation (Pitch Kick):

    -Shortly after liftoff, the rocket performs a small commanded pitch kick

    -This mimics Falcon 9’s early guidance input (~T+10–30s)

    -Pitch changes gradually over time, not instantly

Stage 1 Ascent Guidance:

    -After the pitch kick, pitch is ramped by altitude

    -The rocket smoothly transitions from near-vertical to ~47°

    -This represents a simplified gravity turn while thrust is still active

    Stage 2 Guidance:

    -Stage 2 performs its own pitch ramp:

        -Transitions from ~47° toward ~20–25°

    -Pitch is adjusted gradually to build horizontal velocity

    -Fairing mass (~1,750 kg) is jettisoned once at ~110 km altitude

---

Telemetry

Live, terminal-friendly telemetry updated each tick:
```
Time
KINEMATICS:
  Total Velocity
  X / Y Position
  X / Y Velocity
  X / Y Acceleration
  Pitch Angle

AERODYNAMICS:
  Drag
  Dynamic Pressure (Q)

PROPULSION / MASS:
  Thrust
  Fuel Remaining
  Total Mass

FLIGHT STATE:
  Rocket State
  Current Stage
  Next Stage
```

Output updates in place to avoid terminal clutter

Designed for debugging physics and guidance behavior, not visuals

---

Mass Modeling

    -Total mass is computed dynamically from:

    --All attached or ignited stages

    --Payload mass

    -Fairing jettison is modeled explicitly:

    --~1,750 kg removed once during stage 2 ascent

    -Mass changes directly affect acceleration and trajectory

---

    Current Development Phases
Phase 1 — Simulation Foundation ✅

    -Time-stepped loop

    -Rocket state tracking

    -Live CLI telemetry

    -Basic mission success conditions

Phase 2 — Physics-Based Vertical Ascent ✅

    -Newtonian motion

    -Thrust, gravity, mass modeling

    -Acceleration → velocity → altitude integration

Phase 3 — Multi-Stage & Composition ✅

    -Stage objects with independent fuel/mass

    -Proper MECO and separation

    -Non-blocking ignition delays

    -Clean stage handoff

Phase 4 — Guidance & Near-Orbital Flight 🚧 (Current)

    -Explicit pitch kick and ascent guidance

    -Altitude-based pitch ramps

    -Horizontal velocity buildup

    -Fairing jettison modeled

    -Stage 2 ascent profile implemented

Current Limitation

    -The simulation can reach ~290 km altitude

    -Stage 2 guidance can reach ~20° pitch

    However:

        -Full orbital insertion is not yet possible

        -Circular/orbital dynamics are not implemented

        -Below ~20°, the vehicle burns out before:

            --Achieving ~7.7 km/s horizontal velocity

            --Reducing vertical velocity to ~0 m/s

    This limitation is intentional and documented, not a bug.

---

Orbital Insertion Success Criteria (Target)

For a 17,500 kg payload (Falcon 9–class):
```
Parameter	                Target
Altitude	                ~290 km
Horizontal Velocity	        ~7,732 m/s
Vertical Velocity	        ~0 m/s
Flight Path Angle	        0° (relative to horizon)
```
These values define future success conditions once orbital mechanics are implemented.