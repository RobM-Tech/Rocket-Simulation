import math

G = 9.81 #m/s^2


def velocity_to_pitch(vx,vy):
    return math.atan2(vx,vy)

def calc_thrust(T, pitch_angle):
    
    T_x = T * math.cos(pitch_angle)
    T_y = T * math.sin(pitch_angle)
    return T_x, T_y

def dynamic_pressure(vy, y):
    rho = air_density(y)
    current_Q = 0.5 * rho * vy**2
    return current_Q



# Vertical calculate
def air_density(y):
    rho0 = 1.225 # kg/m^3 at sea level
    H = 8500 # scale height in meters
    return rho0 * math.exp(-y / H)

def drag_force(y, vy, ref_area):
    rho = air_density(y)
    C_d = 0.3
    return 0.5 * rho * vy**2 * C_d * ref_area * (-1 if vy > 0 else 1)


def gravity_force(t_mass):
    return t_mass * G

def vertical_net_force(thrust, t_mass, y, vy, ref_area):
    return thrust - gravity_force(t_mass) - drag_force(y, vy, ref_area)
        

def vertical_acceleration(rkt, thrust):
    t_mass = rkt.total_mass
    y = rkt.y
    vy = rkt.vy
    ref_area = rkt.reference_area
    
    return vertical_net_force(thrust, t_mass, y, vy, ref_area) / t_mass

#Horizontal Motion

def horizontal_acceleration(rkt, T_x):
    t_mass = rkt.total_mass
    vx = rkt.vx
    # Horizontal drag based on horizontal velocity only
    rho = air_density(rkt.y)
    C_d = 0.3
    ref_area = rkt.reference_area
    F_dx = 0.5 * rho * vx**2 * C_d * ref_area * (-1 if vx > 0 else 1)

    ax = (T_x + F_dx) / t_mass
    return ax