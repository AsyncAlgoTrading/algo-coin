from utils import struct
from enums import Side


@struct
class RiskRequest:
    side = Side
    volume = float
    price = float


@struct
class RiskResponse:
    side = Side
    volume = float
    price = float
    success = bool
