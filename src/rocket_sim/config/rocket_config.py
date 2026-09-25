from dataclasses import dataclass, field
from rocket_sim.config.stage_config import StageConfig
from rocket_sim.config.guidance_config import StageOneGuidance, StageTwoGuidance, PitchInitiation, StageOneFlightProfile

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
    s1_fp: StageOneFlightProfile
    s2_guidance: StageTwoGuidance



