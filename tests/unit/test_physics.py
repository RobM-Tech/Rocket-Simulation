import math
import pytest

from rocket_sim.physics.physics import total_velocity, air_density

# Test total velocity

def test_total_velocity_direc_doesnt_matter():
    neg_result = total_velocity(vx=-300.00, vy=-300.00)
    pos_result = total_velocity(vx=300.00, vy=300.00)

    expected = 424.2640687

    assert neg_result == pytest.approx(expected)
    assert neg_result == pos_result


def test_total_velocity_one_direc():
    y_result = total_velocity(vx=0.0, vy=300.0)
    x_result = total_velocity(vx=300.0, vy=0.0)

    expected = 300.0

    assert y_result == pytest.approx(expected)
    assert x_result == pytest.approx(expected)

def test_total_velocity_at_rest():
    result = total_velocity(vx=0.0, vy=0.0)

    expected = 0.0

    assert result == expected

# Test air density

def test_air_density_at_sea_level():
    result = air_density(y=0.0)

    expected = 1.225 # kg/m^3 - Sea level reference density

    assert result == pytest.approx(expected)

def test_air_density_below_sea_level():
    result = air_density(y=-100.0)

    expected = 1.225 # kg/m^3 - Sea level reference density
    # This is expected due to clamp in function

    assert result == pytest.approx(expected)

def test_air_density_at_scale_height():
    result = air_density(y=8500.0)

    # ~36% as thick as sea level
    expected = 0.4506 

    assert result == pytest.approx(expected, abs=1e-4)

def test_air_density_max_alt_boundary():
    result = air_density(y=150_000)
    space_result = air_density(y=500_000)

    expected = 0.0 # Code base alt boundary 

    assert result == pytest.approx(expected)
    assert space_result == pytest.approx(expected)