from dataclasses import dataclass

from typing import List


@dataclass
class Prediction:
    outcome: List[str]
    profit: float = 0.0
