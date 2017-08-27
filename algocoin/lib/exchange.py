import json
from abc import abstractmethod
from .config import ExchangeConfig
from .data_source import StreamingDataSource
from .logging import LOG as log
from .enums import TickType
from .define import EXCHANGE_MARKET_DATA_ENDPOINT, EXCHANGE_ORDER_ENDPOINT


class Exchange(StreamingDataSource):
    def __init__(self, options: ExchangeConfig) -> None:
        super(Exchange, self).__init__(options)
        self._lastseqnum = -1
        self._missingseqnum = set()  # type: Set
        self._seqnum_enabled = False
        self._md_url = EXCHANGE_MARKET_DATA_ENDPOINT(options.exchange_type, options.trading_type)
        self._oe_url = EXCHANGE_ORDER_ENDPOINT(options.exchange_type, options.trading_type)
        self._manual = False

        self._pending_orders = {}

    def close(self) -> None:
        log.critical('Closing....')
        self.ws.close()

    def seqnum(self, number: int) -> None:
        if self._lastseqnum == -1:
            # first seen
            self._lastseqnum = number
            return

        if number != self._lastseqnum + 1 and number not in self._missingseqnum:
            log.error('ERROR: Missing sequence number/s: %s' % ','.join(
                str(x) for x in range(self._lastseqnum+1, number+1)))
            self._missingseqnum.update(
                x for x in range(self._lastseqnum+1, number+1))
            log.error(self._missingseqnum)

        if number in self._missingseqnum:
            self._missingseqnum.remove(number)
            log.warning('INFO: Got out of order data for seqnum: %s' % number)

        else:
            self._lastseqnum = number

    def receive(self) -> None:
        res = self.tickToData(json.loads(self.ws.recv()))

        if self._seqnum_enabled and res.type != TickType.HEARTBEAT:
            self.seqnum(res.sequence)

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

    @abstractmethod
    def accounts(self):
        '''account info'''
