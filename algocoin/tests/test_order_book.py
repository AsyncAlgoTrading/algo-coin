import random
from datetime import datetime
from pprint import pprint

from algocoin.lib.order_book import OrderBook
from algocoin.lib.structs import MarketData, Instrument
from algocoin.lib.enums import Side, \
                               OptionSide, \
                               CurrencyType, \
                               PairType, \
                               OrderType, \
                               OrderSubType, \
                               TickType, \
                               TradeResult, \
                               InstrumentType


def generateInstruments(pairs):
    return [Instrument(underlying=pair) for pair in pairs]


def initialMarketData(count, instruments=None):
    instruments = instruments or generateInstruments([PairType.BTCUSD, PairType.ETHUSD])
    ret = []
    for _ in range(count):
        side = random.choice([Side.BUY, Side.SELL])
        volume = random.randrange(0, 500) / 10

        if side == Side.BUY:
            price = random.randrange(5000, 5500) / 10
        if side == Side.SELL:
            price = random.randrange(5501, 6000) / 10

        tick = random.choice([TickType.OPEN, TickType.CHANGE])
        instrument = random.choice(instruments)

        remaining = random.choice([0.0, random.randrange(0, 100)/10])

        if tick == TickType.DONE:
            reason = random.choice(['', 'cancelled', 'done'])
        elif tick == TickType.CHANGE:
            reason = random.choice(['', 'cancelled', 'done'])
        else:
            reason = ''

        sequence = -1
        order_type = OrderType.NONE

        m = MarketData(time=datetime.now(),
                       volume=volume,
                       price=price,
                       type=tick,
                       instrument=instrument,
                       side=side,
                       remaining=remaining,
                       reason=reason,
                       sequence=sequence,
                       order_type=order_type)

        ret.append(m)
    return ret


def generateMarketData(count, instruments=None):
    instruments = instruments or generateInstruments([PairType.BTCUSD, PairType.ETHUSD])
    ret = []
    for _ in range(count):
        side = random.choice([Side.BUY, Side.SELL])

        volume = random.randrange(0, 500) / 10

        if side == Side.BUY:
            price = random.randrange(5000, 5500) / 10
        if side == Side.SELL:
            price = random.randrange(5501, 6000) / 10

        tick = random.choice([TickType.TRADE,
                              TickType.RECEIVED,
                              TickType.OPEN,
                              TickType.DONE,
                              TickType.CHANGE])
        instrument = random.choice(instruments)

        remaining = random.choice([0.0, random.randrange(0, 100)/10])

        if tick == TickType.DONE:
            reason = random.choice(['', 'cancelled', 'done'])
        elif tick == TickType.CHANGE:
            reason = random.choice(['', 'cancelled', 'done'])
        else:
            reason = ''

        sequence = -1
        order_type = OrderType.NONE

        m = MarketData(time=datetime.now(),
                       volume=volume,
                       price=price,
                       type=tick,
                       instrument=instrument,
                       side=side,
                       remaining=remaining,
                       reason=reason,
                       sequence=sequence,
                       order_type=order_type)

        ret.append(m)

    return ret


class TestDataSource:
    def test_order_book(self):
        pairs = [PairType.BTCUSD, PairType.ETHUSD]
        instruments = generateInstruments(pairs)

        ob = OrderBook(instruments)

        for item in initialMarketData(50, instruments):
            ob.push(item)

        print(str(ob))
