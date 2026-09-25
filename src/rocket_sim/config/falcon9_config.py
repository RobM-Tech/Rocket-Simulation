
from rocket_sim.config.rocket_config import RocketConfig
from rocket_sim.config.stage_config import StageConfig
from rocket_sim.config.guidance_config import StageOneGuidance, StageTwoGuidance, PitchInitiation, StageOneFlightProfile

stage1 = StageConfig(dry_mass         = 25_600,
                     fuel_mass        = 409_500, 
                     thrust           = 7_607_000,
                     burn_rate        = 2_600,
                     throttle_percent = 0.8
                     )

stage2 = StageConfig(dry_mass         = 4_000,
                     fuel_mass        = 92_670,
                     thrust           = 981_000,
                     burn_rate        = 257,
                     throttle_percent = 0.8
                     )
stages = []
stages.append(stage1)
stages.append(stage2)

pitch_init = PitchInitiation(starting_pitch  = 0.0, # degree
                             command_pitch   = 8.0,  # degree
                             init_height     = 75,
                             pitch_inc_step  = 0.2
                             )

s1_guidance = StageOneGuidance(s1_throttle_rate_limit  = 0.25,
                               s1_pitch_adjust_limit   = 0.5,    # degree fraction per second
                               s1_max_q_throttle       = 0.70,

                               s1_ramp_dur           = 165,      # s
                               s1_ramp_delay         = 10,       # s
                               s1_min_vel            = 2350,     # m/s
                               s1_sep_min_alt        = 65_000,   # m
                               s1_nominal_burn_time  = 160,      # s
                               s1_start_pitch        = 8.0,      # degree
                               s1_end_pitch          = 66.0,     # degree
                               s1_max_pitch_bias_deg = 5.0,      # degree
                               s1_throttle_dwn_time  = 40,       # s
                               s1_throttle_up_time   = 75,       # s
                               s1_MECO_delay         = 3.0       # s       
                              )

s1_fp = StageOneFlightProfile(pad_clear_duration        = 35.0,    # seconds
                              pad_clear_alt_ceiling     = 2500.0,  # meters
                              pad_clear_accel_trigger   = 2.1,     # m/s^2
                              pad_clear_throttle        = 0.80,

                            
                              transonic_duration_start  = 35.0,    # seconds
                              transonic_duration_end    = 55.0,    # seconds
                              transonic_alt_ceiling     = 5000.0,  # meters
                              transonic_accel_trigger   = 3.3,     # m/s^2
                              transonic_throttle        = 0.75,

                              max_q_start_time          = 35.0,    # seconds
                              max_q_end_time            = 105.0,    # seconds
                              max_q_alt_ceiling         = 25000.0, # meters
                            )

s2_guidance = StageTwoGuidance(s2_ramp_dur                  = 30,      # s
                               s2_ramp_delay                = 5.0,     # s
                               s2_nominal_burn_time         = 360,     # s
                               s2_orbital_velocity          = 7650,    # m/s
                               s2_target_apo                = 295,     
                               s2_vert_catch_pitch          = 78.0,
                               s2_mid_pitch                 = 45.0,
                               s2_end_pitch                 = 90.0,
                               s2_fairing_jettison_height = 110_000, # m
                               s2_max_vert_catch_height     = 145_000, # m
                               s2_pitch_adjust_limit_deg    = 0.025,
                               s2_vert_catch_vy_limit       = 50,
                               s2_ignition_delay            = 3.0
                              )


falcon9_rocket = RocketConfig(ref_area=10.52,
                              payload_weight=17_500.0,
                              fairing_weight=1750,
                              stages=stages,
                              pitch_init=pitch_init,
                              s1_guidance=s1_guidance,
                              s1_fp=s1_fp,
                              s2_guidance=s2_guidance
                              )