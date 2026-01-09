import math

G = 9.81 #m/s^2

def dynamic_pressure(velocity, altitude):
    rho = air_density(altitude)
    current_Q = 0.5 * rho * velocity**2
    return current_Q


# Vertical calculate
def air_density(altitude):
    rho0 = 1.225 # kg/m^3 at sea level
    H = 8500 # scale height in meters
    return rho0 * math.exp(-altitude / H)

def drag_force(altitude, velocity, ref_area):
    rho = air_density(altitude)
    C_d = 0.3
    return 0.5 * rho * velocity**2 * C_d * ref_area * (-1 if velocity > 0 else 1)


def gravity_force(t_mass):
    return t_mass * G

def vertical_net_force(thrust, t_mass, altitude, velocity, ref_area):
    return thrust - gravity_force(t_mass) - drag_force(altitude, velocity, ref_area)
        

def vertical_acceleration(thrust, t_mass, altitude, velocity, ref_area):
     return vertical_net_force(thrust, t_mass, altitude, velocity, ref_area) / t_mass