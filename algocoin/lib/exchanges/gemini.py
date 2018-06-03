import json
from websocket import create_connection
from ..oe.gemini import GeminiSession
from ..config import ExchangeConfig
from ..enums import TradingType, ExchangeType, TickType, TradeResult
from ..exchange import Exchange
from ..structs import TradeRequest, TradeResponse, Account
from ..utils import get_keys_from_environment, str_to_currency_type
from ..logging import LOG as log
from .helpers import GeminiHelpersMixin


class GeminiExchange(GeminiHelpersMixin, Exchange):
    def __init__(self, options: ExchangeConfig) -> None:
        super(GeminiExchange, self).__init__(options)
        self._type = ExchangeType.GEMINI
        self._last = None

        if options.trading_type == TradingType.LIVE:
            self._key, self._secret, self._passphrase = get_keys_from_environment('GEMINI')
            self._client = GeminiSession(api_key=self._key, api_secret=self._secret, sandbox=False)
        elif options.trading_type == TradingType.SANDBOX:
            self._key, self._secret, self._passphrase = get_keys_from_environment('GEMINI_SANDBOX')
            self._client = GeminiSession(self._key, self._secret, sandbox=True)

        val = self._client.get_balances() if hasattr(self, '_client') else ['BACKTEST']

        self._accounts = []
        for i, jsn in enumerate(val):
            currency = str_to_currency_type(jsn.get('currency'))
            balance = float(jsn.get('available', 'inf'))
            id = str(i)
            account = Account(id=id, currency=currency, balance=balance)
            self._accounts.append(account)

        # self._subscription = json.dumps({"type": "subscribe",
        #                                  "product_id": "BTC-USD"})
        # self._heartbeat = json.dumps({"type": "heartbeat",
        #                               "on": True})

        self._seqnum_enabled = False

    def run(self, engine) -> None:
        # DEBUG
        # websocket.enableTrace(True)

        while True:
            if not self._running and not self._manual:
                # startup and redundancy
                log.info('Starting....')
                self.ws = create_connection(self._md_url)
                log.info('Connected!')

                # self.ws.send(self._subscription)
                # log.info('Sending Subscription %s' % self._subscription)
                # self.ws.send(self._heartbeat)
                # log.info('Sending Heartbeat %s' % self._subscription)

                self._running = True

                log.info('')
                log.info('Starting algo trading')
            try:
                while True:
                    self.receive()

            except KeyboardInterrupt:
                log.critical('Terminating program')
                engine.terminate()
                return
        return self._accounts

    def orderBook(self, level=1):
        '''get order book'''
        return self._client.getProductOrderBook(level=level)

    def buy(self, req: TradeRequest) -> TradeResponse:
        '''execute a buy order'''
        params = GeminiExchange.trade_req_to_params(req)
        # log.warn("Buy params: %s", str(params))
        order = self._client.new_order(params['product_id'],
                                       params['size'],
                                       params['price'],
                                       'buy',
                                       client_order_id=None,
                                       order_execution=None)

        '''{
            "avg_execution_price": "0.00",
            "client_order_id": "20170208_example",
            "exchange": "gemini",
            "executed_amount": "0",
            "id": "372456298",
            "is_cancelled": false,
            "is_hidden": false,
            "is_live": true,
            "order_id": "372456298",
            "original_amount": "14.0296",
            "price": "1059.54",
            "remaining_amount": "14.0296",
            "side": "buy",
            "symbol": "btcusd",
            "timestamp": "1478203017",
            "timestampms": 1478203017455,
            "type": "exchange limit",
            "was_forced": false
        }'''
        # FIXME check these
        if order.get('result') == 'error':
            log.critical("Order Error - %s" % order)
            raise Exception('Order Error!')

        executed_amount = float(order['executed_amount'])
        remaining_amount = float(order['remaining_amount'])
        avg_execution_price = float(order['avg_execution_price'])

        slippage = float(params['price'])-avg_execution_price if executed_amount > 0.0 else 0.0
        txn_cost = 0.0
        status = TradeResult.NONE

        if (req.volume - executed_amount) < 0.001:
            status = TradeResult.FILLED
        elif order.get('is_cancelled', ''):
            status = TradeResult.REJECTED
        elif remaining_amount > 0.0:
            status = TradeResult.PARTIAL
        else:
            status = TradeResult.PENDING

        resp = TradeResponse(request=req,
                             side=req.side,
                             volume=executed_amount,
                             price=avg_execution_price,
                             currency=req.currency,
                             slippage=slippage,
                             transaction_cost=txn_cost,
                             status=status,
                             order_id=order['order_id'],
                             remaining=remaining_amount,
                             )
        return resp

    def sell(self, req: TradeRequest) -> TradeResponse:
        '''execute a sell order'''
        params = GeminiExchange.trade_req_to_params(req)
        # log.warn("Sell params: %s", str(params))
        order = self._client.new_order(params['product_id'],
                                       params['size'],
                                       params['price'],
                                       'sell',
                                       client_order_id=None,
                                       order_execution=None)

        if order.get('result') == 'error':
            log.critical("Order Error - %s" % order)
            raise Exception('Order Error!')

        executed_amount = float(order['executed_amount'])
        remaining_amount = float(order['remaining_amount'])
        avg_execution_price = float(order['avg_execution_price'])

        slippage = float(params['price'])-avg_execution_price if executed_amount > 0.0 else 0.0
        txn_cost = 0.0
        status = TradeResult.NONE

        if (req.volume - executed_amount) < 0.001:
            status = TradeResult.FILLED
        elif order.get('is_cancelled', ''):
            status = TradeResult.REJECTED
        elif remaining_amount > 0.0:
            status = TradeResult.PARTIAL
        else:
            status = TradeResult.PENDING

        resp = TradeResponse(request=req,
                             side=req.side,
                             volume=executed_amount,
                             price=avg_execution_price,
                             currency=req.currency,
                             slippage=slippage,
                             transaction_cost=txn_cost,
                             status=status,
                             order_id=order['order_id'],
                             remaining=remaining_amount,
                             )
        return resp

    def receive(self) -> None:
        jsn = json.loads(self.ws.recv())
        if jsn.get('type') == 'heartbeat':
            pass
        else:
            for item in jsn.get('events'):
                res = self.tickToData(item)

                if not self._running:
                    pass

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
