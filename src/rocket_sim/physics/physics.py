import math

# =====================================================================
# 1. PLANETARY PARAMETERS & PHYSICAL CONSTANTS
# =====================================================================
gravity = 9.81                # m/s^2 - Standard acceleration at sea level
G = 6.6743 * 10**-11          # m^3/kg/s^2 - Universal gravitational constant
M_e = 5.972 * 10**24          # kg - Total planetary mass of Earth
R_e = 6.371 * 10**6           # m - Volumetric mean radius of Earth

# =====================================================================
# 2. FORCE & VECTOR MATHEMATICS UTILITIES
# =====================================================================

def update_r(y):
    """Calculates absolute scalar distance from the vehicle to Earth's center."""
    return R_e + y


def gravity_unit_vec(x, y, r):
    """Generates directional unit components pointing directly to planetary center."""
    G_x = -x / r
    G_y = -(R_e + y) / r
    return G_x, G_y


def velocity_unit_vec(vx, vy, t_velocity): 
    """Normalizes the direction of travel. Prevents ZeroDivisionError if stationary."""
    if t_velocity == 0:
        return 0.0, 0.0
    V_x = -vx / t_velocity 
    V_y = -vy / t_velocity 
    return V_x, V_y


def total_velocity(vx, vy):
    """Calculates absolute velocity magnitude from horizontal and vertical components."""
    return math.sqrt((vx**2) + (vy**2))


def total_accel(ay, ax):
    """Calculates total instantaneous scalar acceleration vector magnitude."""
    return math.sqrt(ay**2 + ax**2)


def velocity_to_pitch(vx, vy):
    """Computes the instantaneous velocity vector flight-path angle in radians."""
    return math.atan2(vx, vy)


# =====================================================================
# 3. ATMOSPHERIC & ENVIRONMENTAL MODELS
# =====================================================================

def air_density(y):
    """Models atmospheric density decay using barometric scale height.
    
    Clamps bounds early to avoid mathematical domain errors at flight extremes.
    """
    if y < 0:
        y = 0.0
    if y > 150_000:
        return 0.0

    rho0 = 1.225   # kg/m^3 - Sea level reference density
    H = 8500       # m - Scale height for exponential decay model
    return rho0 * math.exp(-y / H)


def dynamic_pressure(v_total, y):
    """Calculates aerodynamic dynamic pressure (Q) relative to speed vector."""
    rho = air_density(y)
    return 0.5 * rho * v_total**2


# =====================================================================
# 4. ENVIRONMENTAL & PROPULSION FORCE RESOLUTIONS
# =====================================================================

def calc_thrust(T, pitch_angle):
    """Resolves net thrust along current guidance orientation vector framework.
    
    Assumes pitch_angle = 0° points straight up, turning clockwise toward 90° (horizontal).
    """
    T_x = T * math.sin(pitch_angle)   # Horizontal thrust projection
    T_y = T * math.cos(pitch_angle)   # Vertical thrust projection
    return T_x, T_y


def gravity_force(t_mass, y, x):
    """Calculates gravitational force vectors via Newton's Law of Universal Gravitation."""
    r = math.sqrt(x**2 + update_r(y)**2)
    gravity_mag = G * (M_e * t_mass) / r**2
    G_x, G_y = gravity_unit_vec(x, y, r)

    Fg_x = gravity_mag * G_x 
    Fg_y = gravity_mag * G_y 
    
    return Fg_y, Fg_x


def centripetal_force(t_mass, t_velocity, y):
    """Computes outward apparent force vector scaling over Earth's curved radius profile."""
    return t_mass * t_velocity**2 / update_r(y)


def drag_force(y, t_velocity, ref_area, vx, vy):
    """Calculates fluid dynamic drag forces directly opposing motion direction.
    
    Implements a simple transonic drag modification near the speed of sound (Mach 1).
    """
    if t_velocity == 0:
        return 0.0, 0.0

    rho = air_density(y)
    mach = t_velocity / 343.0

    # Simple transonic wave-drag scaling curve
    C_d = 0.3
    if 0.8 < mach < 1.2:
        C_d = 0.4             # Transonic barrier structural resistance spike
    elif mach >= 1.2:
        C_d = 0.4             # Supersonic equalization index
        
    drag = 0.5 * rho * t_velocity**2 * C_d * ref_area

    drag_x = -drag * (vx / t_velocity)
    drag_y = -drag * (vy / t_velocity)

    return drag_y, drag_x


# =====================================================================
# 5. KINEMATICS RESOLUTION CORE ENGINE
# =====================================================================

def net_force(T_y, T_x, vx, vy, t_mass, y, x, t_velocity, ref_area):
    """Unifies propulsive, gravitational, and fluid forces into global net results."""
    drag_y, drag_x = drag_force(y, t_velocity, ref_area, vx, vy)
    Fg_y, Fg_x = gravity_force(t_mass, y, x)

    net_force_y = T_y + Fg_y + drag_y
    net_force_x = T_x + Fg_x + drag_x

    return net_force_y, net_force_x


def acceleration(t_mass, y, x, vy, vx, ref_area, t_velocity, T_y, T_x):
    """Resolves net forces down to Cartesian acceleration vectors using F=ma (Newton's 2nd)."""
    net_force_y, net_force_x = net_force(T_y, T_x, vx, vy, t_mass, y, x, t_velocity, ref_area)

    ay = net_force_y / t_mass
    ax = net_force_x / t_mass

    return ay, ax


# =====================================================================
# 6. EARTH-CENTERED GUIDANCE COMPLEMENTS
# =====================================================================

def earth_centered_pos(y, x):
    """Calculates localized position unit direction vectors from Earth core origin."""
    rx = x
    ry = R_e + y
    r = math.sqrt(rx*rx + ry*ry)
    return rx / r, ry / r


def radial_velocity(y, x, vx, vy):
    """Computes specific velocity working purely away or toward planet center."""
    r_hat_x, r_hat_y = earth_centered_pos(y, x)
    return vx * r_hat_x + vy * r_hat_y