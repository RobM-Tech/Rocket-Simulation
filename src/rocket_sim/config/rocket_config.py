from dataclasses import dataclass, field
from rocket_sim.config.stage_config import StageConfig
from rocket_sim.config.guidance_config import StageOneGuidance, StageTwoGuidance, PitchInitiation

@dataclass
class RocketConfig:
    # ────────────────────────────────────────────────
    #  Payload & ejectables
    # ────────────────────────────────────────────────
    ref_area: float
    payload_weight: float
    fairing_weight: int

    stages: list[StageConfig]

    pitch_init: PitchInitiation

    s1_guidance: StageOneGuidance
    s2_guidance: StageTwoGuidance



