import json
from datetime import datetime
from functools import lru_cache
from websocket import create_connection, WebSocketTimeoutException
from ..config import ExchangeConfig
from ..define import EXCHANGE_MARKET_DATA_ENDPOINT
from ..enums import Side, ExchangeType, OrderType, OrderSubType, PairType, TickType, ChangeReason
from ..exchange import Exchange
from ..logging import LOG as log
from ..structs import MarketData, Instrument, TradeResponse
from ..utils import str_to_currency_pair_type, str_to_side
from .order_entry import CCXTOrderEntryMixin
from .websockets import WebsocketMixin


class GeminiWebsocketMixin(WebsocketMixin):
    @lru_cache(None)
    def subscription(self):
        return [json.dumps({"type": "subscribe", "product_id": GeminiWebsocketMixin.currencyPairToString(x)}) for x in self.options().currency_pairs]

    @lru_cache(None)
    def heartbeat(self):
        return ''

    def run(self, engine) -> None:
        # DEBUG
        options = self.options()

        while True:
            # startup and redundancy
            log.info('Starting....')
            self.ws = [create_connection(EXCHANGE_MARKET_DATA_ENDPOINT(options.exchange_type, options.trading_type) % x) for x in self.subscription()]
            for x in self.subscription():
                log.info('Sending Subscription %s' % x)

            for ws in self.ws:
                ws.settimeout(1)

            log.info('Connected!')
            log.info('')
            log.critical('Starting algo trading')
            try:
                while True:
                    self.receive()

            except KeyboardInterrupt:
                log.critical('Terminating program')
                engine.terminate()
                return
        return self._accounts

    def receive(self) -> None:
        '''gemini has its own receive method because it uses 1 connection per symbol instead of multiplexing'''
        jsns = []
        for i, x in enumerate(self.subscription()):
            try:
                ret = self.ws[i].recv()
                jsns.append((x, json.loads(ret)))
            except WebSocketTimeoutException:
                jsns.append((x, None))

        for pair, jsn in jsns:
            if jsn:
                if jsn.get('type') == 'heartbeat':
                    pass
                else:
                    for item in jsn.get('events'):
                        item['symbol'] = pair
                        res = self.tickToData(item)

                        if not self._running:
                            pass

                        if res.type != TickType.HEARTBEAT:
                            if res.type not in self._messages:
                                self._messages[res.type] = [res]
                            else:
                                self._messages[res.type].append(res)
                            self._messages_all.append(res)

                        if res.type == TickType.TRADE:
                            self._last = res
                            self.callback(TickType.TRADE, res)
                        elif res.type == TickType.RECEIVED:
                            self.callback(TickType.RECEIVED, res)
                        elif res.type == TickType.OPEN:
                            self.callback(TickType.OPEN, res)
                        elif res.type == TickType.DONE:
                            self.callback(TickType.DONE, res)
                        elif res.type == TickType.CHANGE:
                            self.callback(TickType.CHANGE, res)
                        elif res.type == TickType.HEARTBEAT:
                            # TODO anything?
                            pass
                        else:
                            self.callback(TickType.ERROR, res)

    def cancel(self, resp: TradeResponse):
        '''cancel an order'''
        raise NotImplementedError()

    def cancelAll(self) -> None:
        '''cancel all orders'''
        log.critical('Cancelling all active orders')
        self._client.cancel_all_active_orders()

    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        # print(jsn)
        time = datetime.now()
        price = float(jsn.get('price', 'nan'))
        reason = jsn.get('reason', '')
        volume = float(jsn.get('amount', 'nan'))
        typ = GeminiWebsocketMixin.strToTradeType(jsn.get('type'))

        if typ == TickType.CHANGE and not volume:
            delta = float(jsn.get('delta', 'nan'))
            volume = delta
            typ = GeminiWebsocketMixin.reasonToTradeType(reason)

        side = str_to_side(jsn.get('side', ''))
        remaining_volume = float(jsn.get('remaining', 'nan'))

        if reason == 'canceled':
            reason = ChangeReason.CANCELLED
        elif reason == '':
            reason = ChangeReason.NONE
        else:
            reason = ChangeReason.NONE

        sequence = -1

        if 'symbol' not in jsn:
            return

        currency_pair = str_to_currency_pair_type(json.loads(jsn.get('symbol')).get('product_id'))
        instrument = Instrument(underlying=currency_pair)

        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         instrument=instrument,
                         remaining=remaining_volume,
                         reason=reason,
                         side=side,
                         sequence=sequence)
        return ret

    @staticmethod
    def strToTradeType(s: str) -> TickType:
        return TickType(s.upper())

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
    def tradeReqToParams(req) -> dict:
        p = {}
        p['price'] = str(req.price)
        p['size'] = str(req.volume)
        p['product_id'] = GeminiWebsocketMixin.currencyPairToString(req.instrument.currency_pair)
        p['type'] = GeminiWebsocketMixin.orderTypeToString(req.order_type)

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
    def currencyPairToString(cur: PairType) -> str:
        return cur.value[0].value + cur.value[1].value

    @staticmethod
    def orderTypeToString(typ: OrderType) -> str:
        return type.value.lower()


class GeminiExchange(GeminiWebsocketMixin, CCXTOrderEntryMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(GeminiExchange, self).__init__(options)
        self._type = ExchangeType.GEMINI
        self._last = None
