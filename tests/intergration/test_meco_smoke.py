import pytest
from rocket_sim.models import rocket, stage
from rocket_sim.config import falcon9_config, sim_config

def test_meco_smoke():
    rkt = rocket.Rocket(falcon9_config.falcon9_rocket, y=15.0)

    while rkt.state != rocket.rocket_state.STAGE1_SEPARATION or rkt.current_stage.state != rocket.stage_state.MECO:
        rkt.update(sim_config.SimConfig.dt)

        if rkt.t > 250:
            break

    assert rkt.y >= rkt.s1_guidance.s1_sep_min_alt
    assert rkt.state == rocket.rocket_state.STAGE1_SEPARATION
    assert rkt.current_stage.state == rocket.stage_state.MECO
    