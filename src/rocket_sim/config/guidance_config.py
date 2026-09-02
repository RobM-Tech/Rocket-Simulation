from dataclasses import dataclass, field
import math

@dataclass
class GuidanceConfig:
    # ────────────────────────────────────────────────
    #  Attitude & guidance
    # ────────────────────────────────────────────────
    pitch_angle: float = math.radians(0.0)
    command_pitch: float = math.radians(8.0)
    command_pitch_done: bool = False
    est_apo: int = 0

    # ────────────────────────────────────────────────
    #  Tuning parameters — throttling
    # ────────────────────────────────────────────────
    throttle_rate_limit: float    = 0.25    # fraction per second
    max_q_throttle: float         = 0.7
    target_thrust_fraction: float = 1.0     
    curr_thrust_frac: float       = 0.0

    # ────────────────────────────────────────────────
    #  Tuning parameters — Stage 1
    # ────────────────────────────────────────────────
    s1_ramp_dur: int          = 165      # s
    s1_ramp_delay: int        = 10        # s
    s1_min_vel: int           = 2350     # m/s
    s1_sep_min_alt: int       = 65_000   # m
    s1_nominal_burn_time: int = 160      # s
    s1_start_pitch: int       = command_pitch
    s1_end_pitch: float         = math.radians(80.0)
    s1_throttle_dwn_time: int = 50       # s
    s1_throttle_up_time: int  = 85       # s

    # ────────────────────────────────────────────────
    #  Tuning parameters — Stage 2
    # ────────────────────────────────────────────────
    s2_ramp_dur: int          = 30      # s
    s2_ramp_delay: float        = 5.0     # s
    s2_nominal_burn_time: int = 360      # s
    s2_orbital_velocity: int  = 7650     # m/s
    s2_target_apo: int = 295     
    s2_vert_catch_pitch: float  = math.radians(78.0)
    s2_mid_pitch: float         = math.radians(45.0)
    s2_end_pitch: float         = math.radians(90.0)