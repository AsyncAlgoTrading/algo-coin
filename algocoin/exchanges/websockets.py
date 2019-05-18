import json
from abc import abstractstaticmethod
from datetime import datetime
from functools import lru_cache
from websocket import create_connection
from ..data_source import StreamingDataSource
from ..define import EXCHANGE_MARKET_DATA_ENDPOINT
from ..enums import OrderType, OrderSubType, Side, PairType, CurrencyType, TickType, ChangeReason
from ..utils import parse_date, str_to_currency_pair_type, str_to_side, str_to_order_type
from ..structs import MarketData, Instrument
from ..logging import LOG as log


def exchange_type_to_websocket_client(exchange_type):
    if exchange_type == ExchangeType.COINBASE:
        return CoinbaseWebsocketMixin
    raise Exception(f'No websocket client for {exchange_type}')


class WebsocketMixin(StreamingDataSource):
    def run(self, engine):
        '''run the exchange'''

    # internals
    def close(self):
        '''close the websocket'''

    def seqnum(self, number: int):
        '''manage sequence numbers'''

    def receive(self):
        '''receive data and call callbacks'''

    @abstractstaticmethod
    def tickToData(jsn: dict) -> MarketData:
        pass

    @abstractstaticmethod
    def strToTradeType(s: str) -> TickType:
        pass

    @abstractstaticmethod
    def tradeReqToParams(req) -> dict:
        pass

    @staticmethod
    def currencyToString(cur: CurrencyType) -> str:
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

    @abstractstaticmethod
    def currencyPairToString(cur: PairType) -> str:
        pass

    @abstractstaticmethod
    def orderTypeToString(typ: OrderType) -> str:
        pass

    def reasonToTradeType(s: str) -> TickType:
        pass


class CoinbaseWebsocketMixin(StreamingDataSource):
    @lru_cache(None)
    def subscription(self):
        return [json.dumps({"type": "subscribe", "product_id": CoinbaseWebsocketMixin.currencyPairToString(x)}) for x in self.options().currency_pairs]

    @lru_cache(None)
    def heartbeat(self):
        return json.dumps({"type": "heartbeat", "on": True})

    def close(self):
        '''close the websocket'''

    def seqnum(self, number: int):
        '''manage sequence numbers'''

    def receive(self):
        '''receive data and call callbacks'''

    def ws_client(self):
        options = self.options()
        if options.trading_type == TradingType.LIVE or options.trading_type == TradingType.SIMULATION:
            key, secret, passphrase = get_keys_from_environment(options.ccxt_exchange.value)
        elif options.trading_type == TradingType.SANDBOX:
            key, secret, passphrase = get_keys_from_environment(options.ccxt_exchange.value + '_SANDBOX')

        if options.trading_type in (TradingType.LIVE, TradingType.SIMULATION, TradingType.SANDBOX):
            try:
                if options.trading_type in (TradingType.LIVE, TradingType.SIMULATION):
                    client = gdax.AuthenticatedClient(key,
                                                      secret,
                                                      passphrase)
                elif options.trading_type == TradingType.SANDBOX:
                    client = gdax.AuthenticatedClient(key,
                                                      secret,
                                                      passphrase,
                                                      api_url=EXCHANGE_ORDER_ENDPOINT(ExchangeType.COINBASE, TradingType.SANDBOX))
            except Exception:
                raise Exception('Something went wrong with the API Key/Client instantiation')
            return client

        self._seqnum_enabled = False  # FIXME?

    def run(self, engine) -> None:
        # DEBUG
        websocket.enableTrace(True)
        options = self.options()

        while True:
            # startup and redundancy
            log.info('Starting....')
            self.ws = create_connection(EXCHANGE_MARKET_DATA_ENDPOINT(options.ccxt_exchange, options.trading_type))
            log.info('Connected!')

            for sub in self.subscription():
                self.ws.send(sub)
                log.info('Sending Subscription %s' % sub)

            self.ws.send(self.heartbeat())
            log.info('Sending Heartbeat %s' % self.heartbeat())

            log.info('')
            log.info('Starting algo trading')
            try:
                while True:
                    self.receive()

            except KeyboardInterrupt:
                log.critical('Terminating program')
                return

    @staticmethod
    def tickToData(jsn: dict) -> MarketData:
        time = parse_date(jsn.get('time'))
        price = float(jsn.get('price', 'nan'))
        volume = float(jsn.get('size', 'nan'))
        typ = CoinbaseWebsocketMixin.strToTradeType(jsn.get('type'))
        currency_pair = str_to_currency_pair_type(jsn.get('product_id'))

        instrument = Instrument(underlying=currency_pair)

        order_type = str_to_order_type(jsn.get('order_type', ''))
        side = str_to_side(jsn.get('side', ''))
        remaining_volume = float(jsn.get('remaining_size', 0.0))
        reason = jsn.get('reason', '')

        if reason == 'canceled':
            reason = ChangeReason.CANCELLED
        elif reason == '':
            reason = ChangeReason.NONE
        elif reason == 'filled':
            # FIXME
            reason = ChangeReason.NONE
            # reason = ChangeReason.FILLED
        else:
            reason = ChangeReason.NONE

        sequence = int(jsn.get('sequence'))
        ret = MarketData(time=time,
                         volume=volume,
                         price=price,
                         type=typ,
                         instrument=instrument,
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
    def tradeReqToParams(req) -> dict:
        p = {}
        p['price'] = str(req.price)
        p['size'] = str(req.volume)
        p['product_id'] = CoinbaseWebsocketMixin.currencyPairToString(req.instrument.currency_pair)
        p['type'] = CoinbaseWebsocketMixin.orderTypeToString(req.order_type)

        if req.order_sub_type == OrderSubType.FILL_OR_KILL:
            p['time_in_force'] = 'FOK'
        elif req.order_sub_type == OrderSubType.POST_ONLY:
            p['post_only'] = '1'
        return p

    @staticmethod
    def currencyPairToString(cur: PairType) -> str:
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
    def orderTypeToString(typ: OrderType) -> str:
        if typ == OrderType.LIMIT:
            return 'limit'
        elif typ == OrderType.MARKET:
            return 'market'
