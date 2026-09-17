import math
from rocket_sim.config.guidance_config import PitchInitiation

def initialize_pitch(config: PitchInitiation, current_pitch, cmd_pitch_done):
    if current_pitch < math.radians(config.command_pitch):
        current_pitch += math.radians(config.pitch_inc_step)  # increment small step
        return (current_pitch, cmd_pitch_done)
    else:
        cmd_pitch_done = True
        return (current_pitch, cmd_pitch_done)