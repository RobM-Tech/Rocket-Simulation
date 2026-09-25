import pytest
import math
from dataclasses import dataclass
from rocket_sim.guidance.stage_one_guidance import s1_guidance
from rocket_sim.config.guidance_config import StageOneGuidance

@pytest.fixture
def config(): 
    return StageOneGuidance(
                            s1_throttle_rate_limit  = 0.25,
                            s1_pitch_adjust_limit   = 0.5,    # degree fraction per second
                            s1_max_q_throttle       = 0.7,

                            s1_ramp_dur           = 165,      # s
                            s1_ramp_delay         = 10.0,       # s
                            s1_min_vel            = 2350,     # m/s
                            s1_sep_min_alt        = 65_000,   # m
                            s1_nominal_burn_time  = 160,      # s
                            s1_start_pitch        = 8.0,      # degree
                            s1_end_pitch          = 80.0,     # degree
                            s1_max_pitch_bias_deg = 5.0,      # degree
                            s1_MECO_delay         = 3.0       # s       
                            )



def test_s1_before_ramp_holds_start_pitch(config):
    """Before s1_ramp_delay, target is start pitch; one step moves toward it."""
    t = 5.0  # less than ramp_delay (10)
    curr_pitch = 0.0
    throttle = 1.0
    is_throttled = False

    new_pitch = s1_guidance(config, t, curr_pitch, throttle, is_throttled)

    # Should move toward start (8°), not past one max_delta step
    start = math.radians(config.s1_start_pitch)
    max_delta = math.radians(config.s1_pitch_adjust_limit)

    assert new_pitch == pytest.approx(min(start, max_delta))
    assert new_pitch <= start


def test_s1_rate_limit_caps_step(config):
    t = config.s1_ramp_delay + config.s1_ramp_dur
    curr_pitch = math.radians(config.s1_start_pitch)
    max_delta = math.radians(config.s1_pitch_adjust_limit)

    new_pitch = s1_guidance(config, t, curr_pitch, throttle=1.0, is_throttled=False)

    assert abs(new_pitch - curr_pitch) == pytest.approx(max_delta)
    assert new_pitch > curr_pitch


def test_s1_throttle_bias_reduces_target(config):
    t = config.s1_ramp_delay + config.s1_ramp_dur
    curr_pitch = math.radians(config.s1_end_pitch)

    bias_pitch = s1_guidance(config, t, curr_pitch, throttle=0.0, is_throttled=True)
    new_pitch = s1_guidance(config, t, curr_pitch, throttle=1.0, is_throttled=False)

    assert bias_pitch < new_pitch