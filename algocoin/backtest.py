from .lib.config import BacktestConfig
from .lib.data_source import StreamingDataSource
from .lib.logging import LOG as log, DATA as dlog
from .lib.structs import MarketData
from .lib.utils import parse_date
from .lib.enums import PairType, TickType, Side


class Backtest(StreamingDataSource):
    def __init__(self, options: BacktestConfig) -> None:
        super(Backtest, self).__init__()
        self._file = options.file

    def run(self, engine) -> None:
        log.info('Starting....')
        with open(self._file, 'r') as fp:
            for line in fp:
                self.receive(line)
                # engine.tick()
        log.info('Backtest done, running analysis.')

        import ipdb; ipdb.set_trace()
        self.callback(TickType.ANALYZE, None)

        log.info('Analysis completed.')

    def receive(self, line: str) -> None:
        res = line.strip().split(',')

        # TODO allow if market data for bid/ask
        data = MarketData(time=parse_date(res[0]),
                          price=float(res[1]),
                          volume=float(res[2]),
                          type=TickType.TRADE,
                          currency_pair=PairType.BTCUSD,
                          side=Side.NONE)

        if data.type == TickType.TRADE:
            self.callback(TickType.TRADE, data)
            dlog.info(data)

        else:
            self.callback(TickType.ERROR, data)

    def close(self) -> None:
        pass

    def seqnum(self, num: int) -> None:
        pass

    def tickToData(self, tick: str) -> None:
        pass
