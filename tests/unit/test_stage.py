import pytest
import math

from rocket_sim.config.sim_config import SimConfig
from rocket_sim.config.stage_config import StageConfig
from rocket_sim.models.stage import Stage, stage_state

@pytest.fixture
def config():
    return StageConfig(
                     dry_mass         = 25_600,
                     fuel_mass        = 409_500, 
                     thrust           = 7_607_000,
                     burn_rate        = 2_600,
                     throttle_percent = 0.8
                     )

def test_stage_creation(config):
    stage = Stage(config)

    assert stage.state == stage_state.CREATED

def test_stage_fuel_decrease_when_ignited(config):
    dt = 0.01
    stage = Stage(config)
    stage.state = stage_state.IGNITED

    stage.update(dt)

    expected = config.fuel_mass - (config.burn_rate * dt)
    assert stage.current_fuel_mass == pytest.approx(expected)
    assert stage.current_fuel_mass < config.fuel_mass

def test_stage_calc_mass(config):
    stage = Stage(config)

    mass = stage.calc_total_mass()

    expected = config.fuel_mass + config.dry_mass
    assert mass == pytest.approx(expected)

def test_stage_calc_mass_after_burn(config):
    dt = 0.01
    stage = Stage(config)
    stage.state = stage_state.IGNITED
    mass = stage.calc_total_mass()

    stage.update(dt)
    new_mass = stage.calc_total_mass()

    expected = mass - (config.burn_rate * dt)
    assert new_mass == pytest.approx(expected)
    assert new_mass < mass

def test_fuel_empty(config):
    dt = 0.01
    stage = Stage(config)
    stage.state = stage_state.IGNITED
    stage.current_fuel_mass = -1.0

    stage.update(dt)

    assert stage.current_fuel_mass == pytest.approx(0)
    assert stage.state == stage_state.BURNED_OUT