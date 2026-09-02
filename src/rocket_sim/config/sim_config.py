from dataclasses import dataclass, field
import time
@dataclass
class SimConfig:
    # ────────────────────────────────────────────────
    #  Simulation control & book-keeping
    # ────────────────────────────────────────────────
    t: float = 0.0
    sim_running: bool = False
    orbit_initialized: bool = False
    max_Q: float = 0.0
    max_G: float = 3.5 * 9.81
    g_limit: float = 30.0

    # ────────────────────────────────────────────────
    #  Target & orbit parameters
    # ────────────────────────────────────────────────
    target_orbit_altitude: int = 290_000