from dataclasses import dataclass, field
import time
@dataclass
class SimConfig:
    # ────────────────────────────────────────────────
    #  Simulation control & book-keeping
    # ────────────────────────────────────────────────
    max_G: float = 3.5 * 9.81
    g_limit: float = 30.0

    # ────────────────────────────────────────────────
    #  Target & orbit parameters
    # ────────────────────────────────────────────────
    target_orbit_altitude: int = 290_000


    # ────────────────────────────────────────────────
    #  CLI parameters
    # ────────────────────────────────────────────────
    max_sim_time = 3_600
    dt =  0.01  # Time step in seconds
    cd = 1 #Launch count down time