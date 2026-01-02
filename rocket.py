class Rocket:
    def __init__(self, velocity, altitude, acceleration, mass, thrust):
        self.velocity = velocity #Initial velocity in m/s
        self.altitude = altitude #KSC launch pad altitude in meters
        self.acceleration = acceleration #Initial acceleration in m/s^2
        self.mass = mass #Mass in kg
        self.thrust = thrust #Thrust in Newtons
        

    def calc_weight(self):
        weight = self.mass * 9.81
        return weight

    def calc_net_force(self):
        weight = self.calc_weight()
        netForce = self.thrust - weight
        return netForce

    def calc_acceleration(self):
        netForce = self.calc_net_force()
        self.acceleration = netForce / self.mass


    def update(self, dt):
        self.calc_acceleration()
        self.velocity += self.acceleration * dt #Update velocity based on acceleration and time step
        self.altitude += self.velocity * dt #Update altitude based on velocity and time step
        if self.altitude < 15:
            self.altitude = 15 #Ensure altitude does not go below KSC launch pad altitude for testing purposes



    def get_telemetry(self):
        telemetry = (
                     f"| Velocity: {self.velocity:.2f} m/s "
                     f"| Altitude: {self.altitude:.2f} m "
                     f"| Acceleration: {self.acceleration:.2f} m/s^2 "
                     f"| Mass: {self.mass:.2f} kg "
                     f"| Thrust {self.thrust} N |"
                     )
        return telemetry