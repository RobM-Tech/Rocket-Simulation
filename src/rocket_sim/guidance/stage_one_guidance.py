import math
from rocket_sim.config.guidance_config import StageOneGuidance

def s1_guidance(config: StageOneGuidance, t, curr_pitch, throttle, is_throttled: bool):
        time_since_launch = t
        start = math.radians(config.s1_start_pitch)
        end = math.radians(config.s1_end_pitch)

        if time_since_launch > config.s1_ramp_delay:
            k = min((time_since_launch - config.s1_ramp_delay) / config.s1_ramp_dur, 1)
            target_pitch = start + k * (end - start)
        else:
            target_pitch = start

        if is_throttled:
            
            pitch_bias = math.radians(config.s1_max_pitch_bias_deg) * (1 - throttle)
            target_pitch -= pitch_bias

        # Smooth approach (avoid jumps)
        max_delta = math.radians(config.s1_pitch_adjust_limit)  # max pitch change per timestep
        delta_pitch = target_pitch - curr_pitch
        delta_pitch = max(min(delta_pitch, max_delta), -max_delta)
        curr_pitch += delta_pitch

        return curr_pitch