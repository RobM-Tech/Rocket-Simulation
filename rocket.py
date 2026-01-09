import physics
from stage import stage_state, Stage, empty_stage
from enum import Enum

class rocket_state(Enum):
    IDLE = 1
    LAUNCH = 2
    ASCENT_BURN = 3
    STAGE1_SEPARATION = 4
    COAST = 5
    STAGE2_IGNITION = 6
    

class Rocket:
    def __init__(self, x=0.0, y=0.0, vx=0.0, vy=0.0, ax=0.0, ay=0.0, ref_area=0.0):
        self.state = rocket_state.IDLE
        #Vertical motion
        self.vy = vy #Initial velocity in m/s
        self.ay = ay #Initial acceleration in m/s^2
        self.y = y #in meters

        #Horizontal motion
        self.vx = vx
        self.ax = ax
        self.x = x 
        
        self.reference_area = ref_area
        self.stage_sep_velocity = 2000 #m/s
        self.stage1_sep_altitude = 80000 #in meters, 80km 
        self.time_since_sep = 0
        self.MECO_delay = 4 #separation happens ~4 seconds after MECO
        self.stage2_ignition_delay = 11 # stage 2 ignites ~11 seconds after seperation
        self.current_stage = None
        self.next_stage = None
        self.stages = []

    @property
    def total_mass(self):
        return sum(stage.calc_total_mass() for stage in self.stages if stage.is_attached() or stage.is_ignited())
    
    def __repr__(self):
        return f"Rocket(State: {self.state.name}, Current Stage: {self.current_stage.state.name}, Next Stage: {self.next_stage.state.name})"

    #Main loop
    def update(self, dt):
        self.set_rocket_state(dt)
        self.current_stage.update(dt)

        #Update physics
        thrust = self.current_stage.thrust if self.current_stage else 0
        self.ay = physics.vertical_acceleration(thrust=thrust, t_mass=self.total_mass, altitude=self.y, velocity=self.vy, ref_area=self.reference_area)

        self.vy += self.ay * dt #Update velocity based on acceleration and time step
        self.y += self.vy * dt #Update altitude based on velocity and time step
        if self.y < 0:
            return print("Critical Error, CRASH")
            
        
    
    #Receive telemetry data and format in to readable data
    def get_telemetry(self):
        t_mass = self.total_mass
        thrust = 0.0
        fuel = 0.0

        drag = physics.drag_force(self.y, self.vy, self.reference_area) / 1000  # kN
        Q = physics.dynamic_pressure(velocity=self.vy, altitude=self.y)        # Pa

        if self.current_stage is not None:
            thrust = self.current_stage.thrust
            fuel = self.current_stage.fuel_mass

        telemetry = (
            f"KINEMATICS:\n"
            f"  y:   {self.y:10.2f} m\n"
            f"  Vy:  {self.vy:10.2f} m/s\n"
            f"  Ay:  {self.ay:10.2f} m/s²\n"
            f"\n"
            f"AERODYNAMICS:\n"
            f"  Drag: {drag:10.2f} kN\n"
            f"  Q:    {Q:10.2f} Pa\n"
            f"\n"
            f"PROPULSION / MASS:\n"
            f"  Thrust: {thrust:10.0f} N\n"
            f"  Fuel:   {fuel:10.2f} kg\n"
            f"  Mass:   {t_mass:10.2f} kg\n"
            f"\n"
            f"FLIGHT STATE:\n"
            f"  Rocket State: {self.state}\n"
            f"  Current Stage: {self.current_stage.state if self.current_stage else 'None'}\n"
            f"  Next Stage:    {self.next_stage.state if self.next_stage else 'None'}\n"
        )

        return telemetry


    
    #Rocket state machine

    def set_rocket_state(self, dt):
        match self.state:
            case rocket_state.IDLE:
                self.set_current_stage()
                self.state = rocket_state.LAUNCH

            case rocket_state.LAUNCH:
                self.current_stage.state = stage_state.IGNITED
                if self.ay > 5:
                    self.state = rocket_state.ASCENT_BURN
                

            case rocket_state.ASCENT_BURN:
                if self.y >= self.stage1_sep_altitude and self.vy >= self.stage_sep_velocity:
                    self.state = rocket_state.STAGE1_SEPARATION
                    self.current_stage.state = stage_state.MECO

            case rocket_state.STAGE1_SEPARATION:
                self.time_since_sep += dt
                if self.current_stage.is_meco():
                    
                    if self.time_since_sep >= self.MECO_delay:
                        self.detach_stage(self.current_stage)
                        self.current_stage = self.next_stage
                        self.next_stage = empty_stage()
                        self.next_stage.state = stage_state.EMPTY
                        self.state = rocket_state.COAST

            case rocket_state.COAST:
                self.time_since_sep += dt
                if self.time_since_sep >= self.stage2_ignition_delay:
                    self.state = rocket_state.STAGE2_IGNITION

            case rocket_state.STAGE2_IGNITION:
                self.current_stage.state = stage_state.IGNITED

            case _:
                pass

    #Helpers

    def stage_is_eligible(self, stage):
        if (stage.state in (stage_state.ATTACHED, stage_state.IGNITED)
            and stage.fuel_mass > 0):
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
        return self.state == rocket_state.LAUNCH
    
    def is_ascent_burn(self):
        return self.state == rocket_state.ASCENT_BURN
        
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