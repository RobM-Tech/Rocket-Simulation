from dataclasses import dataclass, field
import math

@dataclass
class GuidanceConfig:
    # ────────────────────────────────────────────────
    #  Tuning parameters — throttling
    # ────────────────────────────────────────────────
    throttle_rate_limit: float    = 0.25    # fraction per second
    max_q_throttle: float         = 0.7

    # ────────────────────────────────────────────────
    #  Tuning parameters — Stage 1
    # ────────────────────────────────────────────────
    s1_ramp_dur: float          = 165      # s
    s1_ramp_delay: float        = 10        # s
    s1_min_vel: float           = 2350     # m/s
    s1_sep_min_alt: float       = 65_000   # m
    s1_nominal_burn_time: float = 160      # s
    s1_start_pitch: float       = math.radians(8.0)
    s1_end_pitch: float         = math.radians(80.0)
    s1_throttle_dwn_time: float = 50       # s
    s1_throttle_up_time: float  = 85       # s

    # ────────────────────────────────────────────────
    #  Tuning parameters — Stage 2
    # ────────────────────────────────────────────────
    s2_ramp_dur: float          = 30      # s
    s2_ramp_delay: float        = 5.0     # s
    s2_nominal_burn_time: float = 360      # s
    s2_orbital_velocity: float  = 7650     # m/s
    s2_target_apo: float = 295     
    s2_vert_catch_pitch: float  = math.radians(78.0)
    s2_mid_pitch: float         = math.radians(45.0)
    s2_end_pitch: float         = math.radians(90.0)