from enum import Enum
from rocket_sim.config.stage_config import StageConfig

class stage_state(Enum):
    CREATED = 1
    ATTACHED = 2
    IGNITED = 3
    THROTTLE_DOWN = 4
    BURNED_OUT = 5
    MECO = 6
    SECO = 7
    SEPARATED = 8
    EMPTY = 9



# Define a stage that Rocket() gets data from
class Stage:
    def __init__(self, config: StageConfig):
        self.state = stage_state.CREATED
        self.stage_config = config
        self.current_burn_rate = 0
        self.throttle = 1.0
        self.throttled_burn_rate = self.stage_config.burn_rate * 0.8
        

    @property
    def thrust(self):
        if ((self.is_throttled() or self.is_ignited()) 
            and not self.is_burned_out()
        ):
            return self.stage_config.thrust * self.throttle
        else:
            return 0
        
    def __repr__(self):
        return f"Stage(state='{self.state.name}')"
        
    def calc_total_mass(self):
        return self.stage_config.fuel_mass + self.stage_config.dry_mass
    

    def update(self, dt):
        if self.is_ignited() or self.is_throttled() and self.stage_config.fuel_mass > 0:
            self.current_burn_rate = self.stage_config.burn_rate * self.throttle

            fuel_consumed = self.current_burn_rate * dt
            self.stage_config.fuel_mass -= fuel_consumed

            if self.stage_config.fuel_mass <= 0:
                self.stage_config.fuel_mass = 0
                self.throttle = 0
                    

    
    #HELPERS

    def is_created(self):
        return self.state == stage_state.CREATED

    def is_attached(self):
        return self.state == stage_state.ATTACHED
    
    def is_ignited(self):
        return self.state == stage_state.IGNITED
    
    def is_throttled(self):
        return self.state == stage_state.THROTTLE_DOWN
    
    def is_burned_out(self):
        return self.state == stage_state.BURNED_OUT
    
    def is_meco(self):
        return self.state == stage_state.MECO
    
    def is_separated(self):
        return self.state == stage_state.SEPARATED

#Void place holder after stage sep
class empty_stage:
    state = stage_state.EMPTY 

    def calc_total_mass(self):
        return 0