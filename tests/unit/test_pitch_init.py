import pytest
import math

from rocket_sim.guidance.pitch_init import initialize_pitch
from rocket_sim.config.guidance_config import PitchInitiation



@pytest.fixture
def config():
    return PitchInitiation(
                            starting_pitch=0.0,
                            command_pitch=8.0,
                            init_height=75,
                            pitch_inc_step=0.2
                            )


def test_pitch_init_reaches_cmd(config):
    pitch = 0.0
    done = False

    # Simulate Sim steps
    for _ in range(100):
        pitch, done = initialize_pitch(config, pitch, done)
        if done:
            break
    assert done is True
    assert pitch == pytest.approx(math.radians(8.0))


def test_pitch_init_start_pitch_above_cmd(config):
    pitch = 12.0
    done = True

    pitch , done = initialize_pitch(config, pitch, done)

    assert pitch == pytest.approx(12)
    assert done is True


def test_pitch_init_step(config):
    pitch = math.radians(5)
    done = False

    new_pitch, done = initialize_pitch(config, pitch, done)

    assert new_pitch == pytest.approx(math.radians(5.2))
    assert done is False

