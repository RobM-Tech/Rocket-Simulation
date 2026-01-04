class Rocket:
    def __init__(self, velocity, altitude, acceleration):
        self.velocity = velocity #Initial velocity in m/s
        self.altitude = altitude #KSC launch pad altitude in meters
        self.acceleration = acceleration #Initial acceleration in m/s^2
        self.stages = []

    @property
    def total_mass(self):
        return sum(stage.calc_total_mass() for stage in self.stages if stage.attached)
    
### Stage states
      
    def attach_stage(self, stage):
        self.stages.append(stage)
        stage.attached = True

    def detach_stage(self, stage):
        pass

### main calculations

    def calc_weight(self):
        weight = self.total_mass * 9.81
        return weight

    def calc_net_force(self):
        weight = self.calc_weight()

        for stage in self.stages:
            if stage.active == True:
                netForce = stage.thrust - weight
            else:
                netForce = 0.00
        
        return netForce

    def calc_acceleration(self):
        for stage in self.stages:
                if self.acceleration > 35:
                    stage.active = False
                else:
                    stage.active = True

        netForce = self.calc_net_force()
        self.acceleration = netForce / self.total_mass
    


    def update(self, dt):

        for stage in self.stages:
            stage.active = True
            stage.update(dt)

        self.calc_acceleration()
        self.velocity += self.acceleration * dt #Update velocity based on acceleration and time step
        self.altitude += self.velocity * dt #Update altitude based on velocity and time step
        if self.altitude < 0:
            return print("Critical Error, CRASH")
            
        
    

    def get_telemetry(self):
        #Receive telemetry data and format in to readable data
        t_mass = self.total_mass
        thrust = 0
        for stage in self.stages:
            thrust = stage.thrust
        telemetry = (
                     f"| Velocity: {self.velocity:.2f} m/s "
                     f"| Altitude: {self.altitude:.2f} m "
                     f"| Acceleration: {self.acceleration:.2f} m/s^2 "
                     f"| Mass: {t_mass:.2f} kg "
                     f"| Thrust {thrust} N |"
                     )
        return telemetry



# Define a stage that Rocket() gets data from
class Stage:
    def __init__(self, dry_mass, fuel_mass, thrust, burn_rate):
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.thrust = thrust
        self.burn_rate = burn_rate
        self.attached = False
        self.active = False
        self.MECO = False


        
    def calc_total_mass(self):
        return self.fuel_mass + self.dry_mass
    

    def update(self, dt):
        if self.active and self.fuel_mass > 0:
            self.fuel_mass -= self.burn_rate * dt
            if self.fuel_mass <= 0:
                self.fuel_mass = 0
                self.active = False

        