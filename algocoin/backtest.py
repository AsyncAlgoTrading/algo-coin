from .lib.config import BacktestConfig
from .lib.data_source import StreamingDataSource
from .lib.logging import LOG as log, DATA as dlog
from .lib.structs import MarketData
from .lib.utils import parse_date
from .lib.enums import CurrencyType, TickType


class Backtest(StreamingDataSource):
    def __init__(self, options: BacktestConfig) -> None:
        super(Backtest, self).__init__()
        self._file = options.file

    def run(self, engine) -> None:
        log.info('Starting....')
        with open(self._file, 'r') as fp:
            for line in fp:
                self.receive(line)
                engine.tick()
        log.info('Backtest done, running analysis.')

        self.callback(TickType.ANALYZE, None)

        log.info('Analysis completed.')

    def receive(self, line: str) -> None:
        res = line.strip().split(',')

        # TODO allow if market data for bid/ask
        data = MarketData(time=parse_date(res[0]),
                          price=float(res[1]),
                          volume=float(res[2]),
                          type=TickType.MATCH,
                          currency=CurrencyType.BTC)

        if data.type == TickType.MATCH:
            self.callback(TickType.MATCH, data)
            dlog.info(data)

        else:
            self.callback(TickType.ERROR, data)

    def close(self):
        pass

    def seqnum(self, num):
        pass

    def tickToData(self, tick):
        pass
