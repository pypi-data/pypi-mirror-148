from dataclasses import dataclass

from core.number.BigFloat import BigFloat


@dataclass
class ExchangeRate:
    currency: str
    to_currency: str
    rate: BigFloat = None
