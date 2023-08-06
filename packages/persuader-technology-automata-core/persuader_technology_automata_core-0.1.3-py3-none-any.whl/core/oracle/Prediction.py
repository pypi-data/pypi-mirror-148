from dataclasses import dataclass

from typing import List


@dataclass
class Prediction:
    outcome: List[str]
    # todo: use enhanced version of Big Float
    profit: float = 0.0
