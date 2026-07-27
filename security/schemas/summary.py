from dataclasses import dataclass


@dataclass
class Summary:
    total: int = 0
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    info: int = 0
