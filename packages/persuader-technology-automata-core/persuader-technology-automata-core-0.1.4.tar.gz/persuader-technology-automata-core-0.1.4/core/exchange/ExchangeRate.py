from dataclasses import dataclass

from core.number.BigFloat import BigFloat


@dataclass
class ExchangeRate:
    instrument: str
    to_instrument: str
    rate: BigFloat = None

    def __iter__(self):
        return iter((self.instrument, self.to_instrument, self.rate))
