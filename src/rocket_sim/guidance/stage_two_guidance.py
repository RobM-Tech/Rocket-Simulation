import math
from rocket_sim.config.guidance_config import StageTwoGuidance

def s2_guidance(config: StageTwoGuidance, curr_pitch, est_apo, y, vy):
    mid = math.radians(config.s2_mid_pitch)
    end = math.radians(config.s2_end_pitch)
    catch = math.radians(config.s2_vert_catch_pitch)

    if est_apo < config.s2_target_apo:
        target_pitch = mid
    elif y < config.s2_max_vert_catch_height and vy < config.s2_vert_catch_vy_limit:
        target_pitch = catch
    else:
        target_pitch = end


    # Smooth approach (avoid jumps)
    max_delta = math.radians(config.s2_pitch_adjust_limit_deg)
    delta_pitch = target_pitch - curr_pitch
    delta_pitch = max(min(delta_pitch, max_delta), -max_delta)
    curr_pitch += delta_pitch

    return curr_pitch