import pytest
import math
from dataclasses import dataclass
from rocket_sim.guidance.stage_two_guidance import s2_guidance
from rocket_sim.config.guidance_config import StageTwoGuidance

@pytest.fixture
def config():
    return StageTwoGuidance(
                            s2_ramp_dur                  = 30,      # s
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


def test_s2_guidance_mid_pitch(config):
    est_apo = 200
    y = 100_000
    vy = 4500
    curr_pitch = math.radians(80.0)
    max_delta = math.radians(config.s2_pitch_adjust_limit_deg)

    new_pitch = s2_guidance(config, curr_pitch, est_apo, y, vy)

    assert new_pitch < curr_pitch
    assert abs(new_pitch - curr_pitch) == pytest.approx(max_delta)


def test_s2_guidance_catch_pitch(config):
    est_apo = 300
    y = 100_000
    vy = 40
    curr_pitch = math.radians(config.s2_mid_pitch)
    max_delta = math.radians(config.s2_pitch_adjust_limit_deg)

    new_pitch = s2_guidance(config, curr_pitch, est_apo, y, vy)

    assert new_pitch > curr_pitch
    assert abs(new_pitch - curr_pitch) == pytest.approx(max_delta)

def test_s2_guidance_end_pitch(config):
    est_apo = 300
    y = 200_000
    vy = 500
    curr_pitch = math.radians(config.s2_vert_catch_pitch)
    max_delta = math.radians(config.s2_pitch_adjust_limit_deg)

    new_pitch = s2_guidance(config, curr_pitch, est_apo, y, vy)

    assert new_pitch > curr_pitch
    assert abs(new_pitch - curr_pitch) == pytest.approx(max_delta)