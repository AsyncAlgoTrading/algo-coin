from .lib.config import BacktestConfig
from .lib.data_source import StreamingDataSource
from .lib.logging import LOG as log, DATA as dlog
from .lib.structs import MarketData
from .lib.utils import parse_date
from .lib.enums import CurrencyType, TickType


class Backtest(StreamingDataSource):
    def __init__(self, options: BacktestConfig):
        super(Backtest, self).__init__()
        self._file = options.file

    def run(self, engine):
        log.info('Starting....')
        with open(self._file, 'r') as fp:
            for line in fp:
                self._receive(line)
                engine.tick()
        log.info('Backtest done, running analysis.')

        self._callback(TickType.ANALYZE, None)

        log.info('Analysis completed.')

    def _receive(self, line: str):
        res = line.strip().split(',')

        # TODO allow if market data for bid/ask
        res = MarketData(time=parse_date(res[0]),
                         price=float(res[1]),
                         volume=float(res[2]),
                         type=TickType.MATCH,
                         currency=CurrencyType.BTC)

        if res.type == TickType.MATCH:
            self._callback(TickType.MATCH, res)
            dlog.info(res)

        else:
            self._callback(TickType.ERROR, res)
