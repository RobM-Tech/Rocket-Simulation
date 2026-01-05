from stage import stage_state, Stage
from enum import Enum

class rocket_state(Enum):
    IDLE = 1
    Launch = 2
    STAGE1_SEPARATION = 3
    STAGE2_IGNITION = 4
    COAST = 5

class Rocket:
    def __init__(self, velocity, altitude, acceleration):
        self.state = rocket_state.IDLE
        self.velocity = velocity #Initial velocity in m/s
        self.staging_velocity = 2000 #m/s
        self.altitude = altitude #in meters
        self.stage1_separation_altitude = 80000 #in meters, 80km 
        self.acceleration = acceleration #Initial acceleration in m/s^2
        self.time_since_stage_detach = 0
        self.MECO_delay = 4 #separation happens ~4 seconds after MECO
        self.stage2_ignition_delay = 15 # stage 2 ignites ~11 seconds after seperation
        self.current_stage = None
        self.next_stage = None
        self.stages = []

    @property
    def total_mass(self):
        return sum(stage.calc_total_mass() for stage in self.stages if stage.is_attached() or stage.is_ignited())
    

    #Main loop
    def update(self, dt):
        self.set_rocket_state(dt)
                            
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
    

    #Helpers

    def set_rocket_state(self, dt):
        match self.state:
            case rocket_state.IDLE:
                self.set_current_stage()
                self.state = rocket_state.Launch

            case rocket_state.Launch:
                self.current_stage.state = stage_state.IGNITED
                if self.altitude >= self.stage1_separation_altitude and self.velocity >= self.staging_velocity:
                    self.state = rocket_state.STAGE1_SEPARATION
                    self.current_stage.state = stage_state.MECO

            case rocket_state.STAGE1_SEPARATION:
                self.time_since_stage_detach += dt
                if self.current_stage.is_meco():
                    
                    if self.time_since_stage_detach >= self.MECO_delay:
                        self.detach_stage(self.current_stage)
                        self.current_stage = self.next_stage
                if self.time_since_stage_detach >= self.stage2_ignition_delay:
                    self.state = rocket_state.STAGE2_IGNITION


            case rocket_state.STAGE2_IGNITION:
                self.current_stage.state = stage_state.IGNITED

            case rocket_state.COAST:
                pass

            case _:
                pass


    def stage_is_eligible(self, stage):
        if stage.state == stage_state.ATTACHED or stage.state == stage_state.IGNITED and stage.fuel_mass > 0:
            return True
        return False
    
    def set_current_stage(self):
        for stage in self.stages:
            if self.current_stage == None and self.stage_is_eligible(stage):
                self.current_stage = stage
            elif self.current_stage != None and self.stage_is_eligible(stage):
                self.next_stage = stage

    def is_idle(self):
        return self.state == rocket_state.IDLE

    def is_launch(self):
        return self.state == rocket_state.Launch
        
    def is_stage1_separation(self):
        return self.state == rocket_state.STAGE1_SEPARATION
    
    def is_stage2_ignition(self):
        return self.state == rocket_state.STAGE2_IGNITION

    def is_coast(self):
        return self.state == rocket_state.COAST

    ### Stage control
      
    def attach_stage(self, stage):
        if self.is_idle():
            self.stages.append(stage)
            stage.state = stage_state.ATTACHED

    def detach_stage(self, stage):
        return self.stages.remove(self.current_stage)