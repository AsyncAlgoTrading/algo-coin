from enums import Side
from utils import struct


@struct
class MarketData:
    pass


@struct
class TradeRequest:
    side = Side
    volume = float
    price = float


@struct
class TradeResponse:
    side = Side
    volume = float
    price = float
    success = bool
