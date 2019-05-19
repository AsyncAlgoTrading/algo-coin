import aiohttp
import json
from abc import abstractstaticmethod, abstractmethod
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
    @abstractmethod
    def subscription(self):
        '''subscription for websocket'''

    @abstractmethod
    def heartbeat(self):
        '''heartbeat for websocket'''

    def seqnum(self, number: int) -> int:
        '''manage sequence numbers'''

    async def close(self) -> None:
        '''close the websocket'''
        await self.ws.close()

    async def run(self, engine) -> None:
        options = self.options()
        session = aiohttp.ClientSession()

        while True:
            # startup and redundancy
            log.info('Starting....')
            self.ws = await session.ws_connect(EXCHANGE_MARKET_DATA_ENDPOINT(self._exchange_type, options.trading_type))
            log.info('Connected!')

            for sub in self.subscription():
                await self.ws.send_str(sub)
                log.info('Sending Subscription %s' % sub)

            if self.heartbeat():
                await self.ws.send_str(self.heartbeat())
                log.info('Sending Heartbeat %s' % self.heartbeat())

            log.info('')
            log.critical(f'Starting algo trading: {self._exchange_type}')
            try:
                while True:
                    await self.receive()

            except KeyboardInterrupt:
                log.critical('Terminating program')
                return

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
