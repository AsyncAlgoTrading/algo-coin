from datetime import datetime
from ..enums import CurrencyType, OrderType, OrderSubType
from ..utils import parse_date, str_to_currency_type, str_to_side, \
    str_to_order_type
from ..structs import MarketData
from ..enums import TickType


class GDAXHelpersMixin(object):
    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        time = parse_date(jsn.get('time'))
        price = float(jsn.get('price', 'nan'))
        volume = float(jsn.get('size', 'nan'))
        typ = GDAXHelpersMixin.strToTradeType(jsn.get('type'))
        currency = str_to_currency_type(jsn.get('product_id'))

        order_type = str_to_order_type(jsn.get('order_type', ''))
        side = str_to_side(jsn.get('side', ''))
        remaining_volume = float(jsn.get('remaining_size', 'nan'))
        reason = jsn.get('reason', '')
        sequence = int(jsn.get('sequence'))

        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         currency=currency,
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
        p['product_id'] = GDAXHelpersMixin.currency_to_string(req.currency)
        p['type'] = GDAXHelpersMixin.order_type_to_string(req.order_type)

        if req.order_sub_type == OrderSubType.FILL_OR_KILL:
            p['time_in_force'] = 'FOK'
        elif req.order_sub_type == OrderSubType.POST_ONLY:
            p['post_only'] = '1'
        return p

    @staticmethod
    def currency_to_string(cur: CurrencyType) -> str:
        if cur == CurrencyType.BTC:
            return 'BTC-USD'

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
        currency = str_to_currency_type('BTC')

        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         currency=currency,
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
        p['product_id'] = GeminiHelpersMixin.currency_to_string(req.currency)
        p['type'] = GeminiHelpersMixin.order_type_to_string(req.order_type)

        if req.order_sub_type == OrderSubType.FILL_OR_KILL:
            p['time_in_force'] = 'FOK'
        elif req.order_sub_type == OrderSubType.POST_ONLY:
            p['post_only'] = '1'
        return p

    @staticmethod
    def currency_to_string(cur: CurrencyType) -> str:
        if cur == CurrencyType.BTC:
            return 'BTCUSD'

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
