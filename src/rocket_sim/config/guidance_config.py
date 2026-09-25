from dataclasses import dataclass, field
import math


@dataclass
class PitchInitiation:
    starting_pitch: float
    command_pitch: float
    init_height: int
    pitch_inc_step: float

@dataclass
class StageOneGuidance:
    # ────────────────────────────────────────────────
    #  Tuning parameters — Stage 1
    # ────────────────────────────────────────────────
    s1_throttle_rate_limit: float
    s1_pitch_adjust_limit: float
    s1_max_q_throttle: float
    s1_ramp_dur: float          
    s1_ramp_delay: float        
    s1_min_vel: float           
    s1_sep_min_alt: float       
    s1_nominal_burn_time: float 
    s1_start_pitch: float       
    s1_end_pitch: float
    s1_max_pitch_bias_deg: float         
    s1_throttle_dwn_time: float 
    s1_throttle_up_time: float
    s1_MECO_delay: float

@dataclass
class StageOneFlightProfile:
    #────────────────────────────────────────────────
    # Flight profile throttling
    #────────────────────────────────────────────────
    # Early Ascent / Pad Clearance Phase
    pad_clear_duration: float       # seconds
    pad_clear_alt_ceiling: float    # meters
    pad_clear_accel_trigger: float  # m/s^2
    pad_clear_throttle: float

    # Intermediate Pitch / Transonic Phase
    transonic_duration_start: float # seconds
    transonic_duration_end: float   # seconds
    transonic_alt_ceiling: float    # meters
    transonic_accel_trigger: float  # m/s^2
    transonic_throttle: float

    # Max-Q Structural Protection Phase
    # UPDATED: Shifted earlier to match your new high-fidelity physics timeline!
    max_q_start_time: float         # seconds
    max_q_end_time: float           # seconds
    max_q_alt_ceiling: float        # meters


@dataclass
class StageTwoGuidance:
    # ────────────────────────────────────────────────
    #  Tuning parameters — Stage 2
    # ────────────────────────────────────────────────
    s2_ramp_dur: float          
    s2_ramp_delay: float        
    s2_nominal_burn_time: float 
    s2_orbital_velocity: float      
    s2_target_apo: float     
    s2_vert_catch_pitch: float
    s2_mid_pitch: float         
    s2_end_pitch: float
    s2_fairing_jettison_height: int
    s2_max_vert_catch_height: int
    s2_pitch_adjust_limit_deg: float
    s2_vert_catch_vy_limit: float
    s2_ignition_delay: float