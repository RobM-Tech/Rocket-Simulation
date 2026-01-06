from enum import Enum

class stage_state(Enum):
    CREATED = 1
    ATTACHED = 2
    IGNITED = 3
    BURNED_OUT = 4
    MECO = 5
    SEPARATED = 6
    EMPTY = 7



# Define a stage that Rocket() gets data from
class Stage:
    def __init__(self, dry_mass, fuel_mass, thrust, burn_rate):
        self.state = stage_state.CREATED
        self.dry_mass = dry_mass
        self.fuel_mass = fuel_mass
        self.thrust = thrust
        self.burn_rate = burn_rate
        
    def __repr__(self):
        return f"Stage(state='{self.state.name}')"
        
    def calc_total_mass(self):
        return self.fuel_mass + self.dry_mass
    

    def update(self, dt):
        if self.is_ignited() and self.fuel_mass > 0:
            self.fuel_mass -= self.burn_rate * dt
            if self.fuel_mass <= 0:
                self.fuel_mass = 0
                self.state = stage_state.BURNED_OUT




    #HELPERS

    def is_created(self):
        return self.state == stage_state.CREATED

    def is_attached(self):
        return self.state == stage_state.ATTACHED
    
    def is_ignited(self):
        return self.state == stage_state.IGNITED
    
    def is_burned_out(self):
        return self.state == stage_state.BURNED_OUT
    
    def is_meco(self):
        return self.state == stage_state.MECO
    
    def is_separated(self):
        return self.state == stage_state.SEPARATED

class empty_stage:
    state = stage_state.EMPTY 

    def calc_total_mass(self):
        return 0