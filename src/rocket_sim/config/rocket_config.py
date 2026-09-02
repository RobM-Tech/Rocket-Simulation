from dataclasses import dataclass, field

@dataclass
class RocketConfig:
    # ────────────────────────────────────────────────
    #  Payload & ejectables
    # ────────────────────────────────────────────────
    ref_area: float = 0.0 
    payload_weight: float = 0.0
    fairing_weight: int = 0
    fairing_jettisoned: bool = False


