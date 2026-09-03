from dataclasses import dataclass, field
from rocket_sim.config.stage_config import StageConfig

@dataclass
class RocketConfig:
    # ────────────────────────────────────────────────
    #  Payload & ejectables
    # ────────────────────────────────────────────────
    ref_area: float
    payload_weight: float
    fairing_weight: int

    stages: list[StageConfig]




