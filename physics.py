import math

gravity = 9.81 #m/s^2
G = 6.6743 * 10**-11 #Gravitational constant
M_e = 5.972 * 10**24
R_e = 6.371 * 10**6 # Earth radius in meters (average from IUGG)

#Force calculations
def update_r(y):
    
    r = R_e + y
    return r


def gravity_unit_vec(x, y, r):
    G_x = -x / r
    G_y = -(R_e + y) / r
    return G_x, G_y


def velocity_unit_vec(vx, vy, t_velocity): 
    if t_velocity == 0:
        return 0.0, 0.0
    else:
        V_x = -vx / t_velocity 
        V_y = -vy / t_velocity 
        return V_x, V_y


def total_velocity(vx, vy):
    return math.sqrt((vx**2) + (vy**2))


def velocity_to_pitch(vx,vy):
    return math.atan2(vx,vy)


def calc_thrust(T, pitch_angle):
    # pitch_angle = 0° → straight up
    # pitch_angle = 90° → horizontal to the right
    T_x = T * math.sin(pitch_angle)   # horizontal
    T_y = T * math.cos(pitch_angle)   # vertical
    return T_x, T_y


def dynamic_pressure(vy, y):
    rho = air_density(y)
    current_Q = 0.5 * rho * vy**2
    return current_Q


def gravity_force(t_mass, y, x):
    r = math.sqrt(x**2 + update_r(y)**2)
    gravity = G*(M_e *t_mass) / r**2
    G_x, G_y = gravity_unit_vec(x, y, r)

    Fg_x = gravity * G_x 
    Fg_y = gravity * G_y 
    
    return Fg_y, Fg_x


def centripetal_force(t_mass, t_velocity, y):
    return t_mass * t_velocity**2 / update_r(y)


def air_density(y):
    rho0 = 1.225 # kg/m^3 at sea level
    H = 8500 # scale height in meters
    rho = rho0 * math.exp(-y / H)
    if y > 150_000:
        return 0.0
    if y < 0:
        y = 0
    if rho == 0:
        return 0.0

    return rho


def drag_force(y, t_velocity, ref_area, vx, vy):
    if t_velocity == 0:
        return 0.0, 0.0

    rho = air_density(y)
    mach = t_velocity / 343.0 # ~Speed of sound

    #simple transonic drag spike
    C_d = 0.3
    if 0.8 < mach < 1.2:
        C_d = 0.4 # The "Sound Barrier" drag increase
    elif mach >= 1.2:
        C_d = 0.4 # Supersonic smoothing
        
    drag = 0.5 * rho * t_velocity**2 * C_d * ref_area

    drag_x = -drag * (vx / t_velocity)
    drag_y = -drag * (vy / t_velocity)

    return drag_y, drag_x



def net_force(T_y, T_x, vx, vy, t_mass, y, x, t_velocity, ref_area):
    drag_y, drag_x = drag_force(y, t_velocity, vx, vy, ref_area)

    Fg_y, Fg_x = gravity_force(t_mass, y, x)

    net_force_y = T_y + Fg_y + drag_y
    net_force_x = T_x + Fg_x + drag_x


    return net_force_y, net_force_x


#Motion  

def acceleration(rkt, T_y, T_x):
    t_mass = rkt.total_mass
    y = rkt.y
    x = rkt.x
    vy = rkt.vy
    vx = rkt.vx
    

    ref_area = rkt.reference_area
    t_velocity = rkt.total_velocity

    net_force_y, net_force_x = net_force(T_y, T_x, vx, vy, t_mass, y, x, t_velocity, ref_area)

    ay = net_force_y / t_mass
    ax = net_force_x / t_mass

    return ay, ax


#Guidence

def earth_centered_pos(y, x):
    rx = x
    ry = R_e + y
    r = math.sqrt(rx*rx + ry*ry)
    r_hat_x = rx / r
    r_hat_y = ry / r
    return r_hat_x, r_hat_y

def radial_velocity(y, x, vx, vy):
    r_hat_x, r_hat_y = earth_centered_pos(y, x)
    return vx * r_hat_x + vy * r_hat_y

