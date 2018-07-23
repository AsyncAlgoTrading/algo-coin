from datetime import datetime
from ..enums import OrderType, OrderSubType, Side, PairType, CurrencyType
from ..utils import parse_date, str_to_currency_type, str_to_currency_pair_type, str_to_side, \
    str_to_order_type
from ..structs import MarketData
from ..enums import TickType

from ._cpp_helpers import test
test()


class GDAXHelpersMixin(object):
    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        time = parse_date(jsn.get('time'))
        price = float(jsn.get('price', 'nan'))
        volume = float(jsn.get('size', 'nan'))
        typ = GDAXHelpersMixin.strToTradeType(jsn.get('type'))
        currency_pair = str_to_currency_pair_type(jsn.get('product_id'))

        order_type = str_to_order_type(jsn.get('order_type', ''))
        side = str_to_side(jsn.get('side', ''))
        remaining_volume = float(jsn.get('remaining_size', 0.0))
        reason = jsn.get('reason', '')
        sequence = int(jsn.get('sequence'))
        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         currency_pair=currency_pair,
                         remaining=remaining_volume,
                         reason=reason,
                         side=side,
                         order_type=order_type,
                         sequence=sequence)
        return ret

    @staticmethod
    def strToTradeType(s: str) -> TickType:
        if s == 'match':
            return TickType.TRADE
        elif s == 'received':
            return TickType.RECEIVED
        elif s == 'open':
            return TickType.OPEN
        elif s == 'done':
            return TickType.DONE
        elif s == 'change':
            return TickType.CHANGE
        elif s == 'heartbeat':
            return TickType.HEARTBEAT
        else:
            return TickType.ERROR

    @staticmethod
    def trade_req_to_params(req) -> dict:
        p = {}
        p['price'] = str(req.price)
        p['size'] = str(req.volume)
        p['product_id'] = GDAXHelpersMixin.currency_pair_to_string(req.currency_pair)
        p['type'] = GDAXHelpersMixin.order_type_to_string(req.order_type)

        if req.order_sub_type == OrderSubType.FILL_OR_KILL:
            p['time_in_force'] = 'FOK'
        elif req.order_sub_type == OrderSubType.POST_ONLY:
            p['post_only'] = '1'
        return p

    @staticmethod
    def currency_to_string(cur: CurrencyType) -> str:
        if cur == CurrencyType.BTC:
            return 'BTC'
        if cur == CurrencyType.ETH:
            return 'ETH'
        if cur == CurrencyType.LTC:
            return 'LTC'
        if cur == CurrencyType.BCH:
            return 'BCH'
        else:
            raise Exception('Pair not recognized: %s' % str(cur))

    @staticmethod
    def currency_pair_to_string(cur: PairType) -> str:
        if cur == PairType.BTCUSD:
            return 'BTC-USD'
        if cur == PairType.BTCETH:
            return 'BTC-ETH'
        if cur == PairType.BTCLTC:
            return 'BTC-LTC'
        if cur == PairType.BTCBCH:
            return 'BTC-BCH'
        if cur == PairType.ETHUSD:
            return 'ETH-USD'
        if cur == PairType.LTCUSD:
            return 'LTC-USD'
        if cur == PairType.BCHUSD:
            return 'BCH-USD'
        if cur == PairType.ETHBTC:
            return 'ETH-BTC'
        if cur == PairType.LTCBTC:
            return 'LTC-BTC'
        if cur == PairType.BCHBTC:
            return 'BCH-BTC'
        else:
            raise Exception('Pair not recognized: %s' % str(cur))

    @staticmethod
    def order_type_to_string(typ: OrderType) -> str:
        if typ == OrderType.LIMIT:
            return 'limit'
        elif typ == OrderType.MARKET:
            return 'market'


class GeminiHelpersMixin(object):
    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        # print(jsn)
        time = datetime.now()
        price = float(jsn.get('price', 'nan'))
        reason = jsn.get('reason', '')
        volume = float(jsn.get('amount', 'nan'))
        typ = GeminiHelpersMixin.strToTradeType(jsn.get('type'))

        if typ == TickType.CHANGE and not volume:
            delta = float(jsn.get('delta', 'nan'))
            volume = delta
            typ = GeminiHelpersMixin.reasonToTradeType(reason)

        side = str_to_side(jsn.get('side', ''))
        remaining_volume = float(jsn.get('remaining', 'nan'))

        sequence = -1
        currency_pair = str_to_currency_type('BTC')

        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         currency_pair=currency_pair,
                         remaining=remaining_volume,
                         reason=reason,
                         side=side,
                         sequence=sequence)
        # print(ret)
        return ret

    @staticmethod
    def strToTradeType(s: str) -> TickType:
        if s == 'trade':
            return TickType.TRADE
        elif s == 'change':
            return TickType.CHANGE
        elif s == 'heartbeat':
            return TickType.HEARTBEAT
        else:
            return TickType.ERROR

    @staticmethod
    def reasonToTradeType(s: str) -> TickType:
        s = s.upper()
        if 'CANCEL' in s:
            return TickType.DONE
        if 'PLACE' in s:
            return TickType.OPEN
        if 'INITIAL' in s:
            return TickType.OPEN

    @staticmethod
    def trade_req_to_params(req) -> dict:
        p = {}
        p['price'] = str(req.price)
        p['size'] = str(req.volume)
        p['product_id'] = GeminiHelpersMixin.currency_pair_to_string(req.currency_pair)
        p['type'] = GeminiHelpersMixin.order_type_to_string(req.order_type)

        if p['type'] == OrderType.MARKET:
            if req.side == Side.BUY:
                p['price'] = 100000000.0
            else:
                p['price'] = .00000001

        if req.order_sub_type == OrderSubType.FILL_OR_KILL:
            p['time_in_force'] = 'FOK'
        elif req.order_sub_type == OrderSubType.POST_ONLY:
            p['post_only'] = '1'
        return p

    @staticmethod
    def currency_pair_to_string(cur: PairType) -> str:
        if cur == PairType.BTCUSD:
            return 'BTCUSD'
        if cur == PairType.ZECUSD:
            return 'ZECUSD'
        if cur == PairType.ZECBTC:
            return 'ZECBTC'
        if cur == PairType.ZECETH:
            return 'ZECETH'
        if cur == PairType.ETHBTC:
            return 'ETHBTC'
        if cur == PairType.ETHUSD:
            return 'ETHUSD'
        else:
            raise Exception('Pair not recognized: %s' % str(cur))

    @staticmethod
    def order_type_to_string(typ: OrderType) -> str:
        if typ == OrderType.LIMIT:
            return 'limit'
        elif typ == OrderType.MARKET:
            return 'market'


class ItBitHelpersMixin(object):
    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        pass

    @staticmethod
    def strToTradeType(s: str) -> TickType:
        return TickType.ERROR


class KrakenHelpersMixin(object):
    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        pass

    @staticmethod
    def strToTradeType(s: str) -> TickType:
        return TickType.ERROR
