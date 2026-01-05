from stage import stage_state, Stage
class Rocket:
    def __init__(self, velocity, altitude, acceleration):
        self.velocity = velocity #Initial velocity in m/s
        self.altitude = altitude 
        self.acceleration = acceleration #Initial acceleration in m/s^2
        self.current_stage = None
        self.stages = []

    @property
    def total_mass(self):
        return sum(stage.calc_total_mass() for stage in self.stages if stage.is_attached() or stage.is_ignited())
    
### Stage states
      
    def attach_stage(self, stage):
        self.stages.append(stage)
        stage.state = stage_state.ATTACHED

    def detach_stage(self, stage):
        pass

### main calculations

    def calc_weight(self):
        weight = self.total_mass * 9.81
        return weight

    def calc_net_force(self):
        weight = self.calc_weight()
        netForce = 0.00
        if self.current_stage != None:
            netforce = self.current_stage.thrust - weight
            return netforce

        
        return netForce

    def calc_acceleration(self):
        netForce = self.calc_net_force()
        self.acceleration = netForce / self.total_mass
    


    def update(self, dt):
                
        for stage in self.stages:
            if self.stage_is_eligible(stage):
                self.current_stage = stage
                break
        self.current_stage.state = stage_state.IGNITED
        self.current_stage.update(dt)

        self.calc_acceleration()
        self.velocity += self.acceleration * dt #Update velocity based on acceleration and time step
        self.altitude += self.velocity * dt #Update altitude based on velocity and time step
        if self.altitude < 0:
            return print("Critical Error, CRASH")
            
        
    

    def get_telemetry(self):
        #Receive telemetry data and format in to readable data
        t_mass = self.total_mass
        thrust = 0
        if self.current_stage != None:
            thrust = self.current_stage.thrust
        
        telemetry = (
                     f"| Velocity: {self.velocity:.2f} m/s "
                     f"| Altitude: {self.altitude:.2f} m "
                     f"| Acceleration: {self.acceleration:.2f} m/s^2 "
                     f"| Mass: {t_mass:.2f} kg "
                     f"| Thrust {thrust} N |"
                     )
        return telemetry


    #Helpers

    def stage_is_eligible(self, stage):
        if stage.state == stage_state.ATTACHED or stage.state == stage_state.IGNITED and stage.fuel_mass > 0:
            return True
        return False

        