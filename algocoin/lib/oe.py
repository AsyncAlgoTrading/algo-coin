import ccxt
from .config import ExchangeConfig
from .exchange import Exchange
from .enums import TradingType, ExchangeType
from .structs import TradeRequest, TradeResponse
from .utils import get_keys_from_environment, trade_req_to_params
from .logging import LOG as log


class OrderEntry(object):
    def __init__(self, options: ExchangeConfig, exchange: Exchange):
        # TODO multi exchange
        self.exchange = exchange

        if options.exchange_type == ExchangeType.GEMINI:
            exchange_name = 'gemini'
        else:
            raise Exception('OrderEntry object cannot be instantiated for exchange %s' % options.exchange_type)

        if options.trading_type == TradingType.SANDBOX:
            self._key, self._secret, self._passphrase = get_keys_from_environment(exchange_name.upper() + '_SANDBOX')
        else:
            self._key, self._secret, self._passphrase = get_keys_from_environment(exchange_name.upper())

        self._client = ccxt.__getattribute__(exchange_name)(({
            'apiKey': self._key,
            'secret': self._secret,
        }))

        if options.trading_type == TradingType.LIVE:
            self._client.urls['api'] = self._client.urls['test']

    def orderBook(self, symbol, level=1):
        '''get order book'''
        # TODO process symbol to string
        if level == 1:
            return self._client.fetchOrderBook(symbol)
        else:
            return self._client.fetchL2OrderBook(symbol)

    def buy(self, req: TradeRequest) -> TradeResponse:
        '''execute a buy order'''
        params = trade_req_to_params(req)
        log.warn("Buy params: %s", str(params))
        # order = self._client.create_order(**params)

        # def create_order(self, symbol, type, side, amount, price=None, params={}):

        # if order.get('result') == 'error':
        #     log.critical("Order Error - %s", order)
        #     raise Exception('Order Error!')

        # executed_amount = float(order['executed_amount'])
        # remaining_amount = float(order['remaining_amount'])
        # avg_execution_price = float(order['avg_execution_price'])

        # slippage = float(params['price'])-avg_execution_price if executed_amount > 0.0 else 0.0
        # txn_cost = 0.0
        # status = TradeResult.NONE

        # if (req.volume - executed_amount) < 0.001:
        #     status = TradeResult.FILLED
        # elif order.get('is_cancelled', ''):
        #     status = TradeResult.REJECTED
        # elif remaining_amount > 0.0:
        #     status = TradeResult.PARTIAL
        # else:
        #     status = TradeResult.PENDING

        # resp = TradeResponse(request=req,
        #                      side=req.side,
        #                      volume=executed_amount,
        #                      price=avg_execution_price,
        #                      currency=req.currency,
        #                      slippage=slippage,
        #                      transaction_cost=txn_cost,
        #                      status=status,
        #                      order_id=order['order_id'],
        #                      remaining=remaining_amount,
        #                      )
        # return resp

    def sell(self, req: TradeRequest) -> TradeResponse:
        '''execute a sell order'''
        params = self.exchange.tradeReqToParams(req)
        log.warn("Sell params: %s", str(params))

    def cancel(self, resp: TradeResponse):
        raise NotImplementedError()

    def cancelAll(self, resp: TradeResponse):
        raise NotImplementedError()
