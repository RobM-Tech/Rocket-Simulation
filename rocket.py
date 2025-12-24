class Rocket:
    def __init__(self, velocity, altitude, acceleration):
        self.velocity = 0 #Initial velocity in m/s
        self.altitude = 15 #KSC launch pad altitude in meters
        self.acceleration = 30.0 #Constant acceleration for testing purposes

    def update(self, dt):
        self.velocity += self.acceleration * dt #Update velocity based on acceleration and time step
        self.altitude += self.velocity * dt #Update altitude based on velocity and time step
        if self.altitude < 15:
            self.altitude = 15 #Ensure altitude does not go below KSC launch pad altitude for testing purposes

    def get_telemetry(self):
        return {
            "velocity": self.velocity,
            "altitude": self.altitude,
            "acceleration": self.acceleration
        }