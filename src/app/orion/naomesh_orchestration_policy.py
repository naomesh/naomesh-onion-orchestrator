from enum import Enum


class EnergyPolicy(Enum):
    GREEN = "green"
    BYPASS = "bypass"


class QualityPolicy(Enum):
    GOOD = "good"
    BAD = "bad"
