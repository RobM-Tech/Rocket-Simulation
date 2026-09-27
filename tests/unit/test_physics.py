import math
import pytest

from rocket_sim.physics.physics import total_velocity, air_density, dynamic_pressure

# Test total velocity

def test_total_velocity_rejects_neg_vx():
    with pytest.raises(ValueError, match="Horizontal velocity cannot be negative; direction is incorrect."):
        total_velocity(vx=-100, vy=300)

def test_total_velocity_rejects_neg_vy():
    with pytest.raises(ValueError, match="Vertical velocity cannot be negative; critical failure, vehicle is falling."):
        total_velocity(vx=100, vy=-100)

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

def test_air_density_at_scale_height():
    result = air_density(y=8500.0)

    # ~36% as thick as sea level
    expected = 0.4506 

    assert result == pytest.approx(expected, abs=1e-4)

def test_air_density_max_alt_boundary():
    result = air_density(y=150_000)
    space_result = air_density(y=500_000)

    expected = 0.0 # Code base alt boundary 

    assert result == pytest.approx(expected, abs=1e-1)
    assert space_result == pytest.approx(expected, abs=1e-1)

# Test dynamic pressure
def test_dynamic_pressure_at_rest():
    result = dynamic_pressure(v_total=0.0, y=0.0)

    expected = 0.0

    assert result == pytest.approx(expected, abs=1e-1)

def test_dynamic_pressure_space():
    result = dynamic_pressure(v_total=7300.0, y=500_000)

    expected = 0.0

    assert result == pytest.approx(expected, abs=1e-1)

def test_dynamic_pressure_normal_flight():
    result = dynamic_pressure(v_total=1500.0, y=65_000)

    expected = 657.9807

    assert result == pytest.approx(expected, abs=1e-4)

def test_dynamic_pressure_neg_alt():
    with pytest.raises(ValueError, match="Altitude cannot be negative"):
        dynamic_pressure(v_total=100.0, y=-10.0)