#from rocket_sim.config.rocket_config import RocketConfig
from rocket_sim.config.stage_config import StageConfig

stage1 = StageConfig(dry_mass  = 25_600,
                     fuel_mass = 409_500, 
                     thrust    = 7_607_000,
                     burn_rate = 2_600
                     )

stage2 = StageConfig(dry_mass  = 4_000,
                     fuel_mass = 92_670,
                     thrust    = 981_000,
                     burn_rate = 257
                     )
