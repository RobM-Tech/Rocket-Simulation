from dataclasses import dataclass, field

@dataclass
class StageConfig:
    dry_mass: float
    fuel_mass: float
    thrust: float 
    burn_rate: float 
    