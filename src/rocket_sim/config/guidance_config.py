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