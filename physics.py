G = 9.81 #m/s^2


# Vertical calculate

def gravity_force(t_mass):
    return t_mass * G

def vertical_net_force(thrust, t_mass):
    return thrust - gravity_force(t_mass)
        

def vertical_acceleration(thrust, t_mass):
     return vertical_net_force(thrust, t_mass) / t_mass