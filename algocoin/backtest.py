from .lib.config import BacktestConfig
from .lib.data_source import StreamingDataSource
from .lib.logging import LOG as log, DATA as dlog
from .lib.structs import MarketData
from .lib.utils import parse_date
from .lib.enums import PairType, TickType, Side


def line_to_data(line):
    if line:
        line = line.strip().split(',')
        data = MarketData(time=parse_date(line[0]),
                          price=float(line[1]),
                          volume=float(line[2]),
                          type=TickType.TRADE,
                          currency_pair=PairType.BTCUSD,
                          side=Side.NONE)
        return data
    return None


class Backtest(StreamingDataSource):
    def __init__(self, options: BacktestConfig) -> None:
        super(Backtest, self).__init__()
        self._file = options.file
        self._files = options.files

    def run(self, engine) -> None:
        log.info('Starting....')

        if self._file:
            with open(self._file, 'r') as fp:
                for line in fp:
                    self.receive(line_to_data(line))

        else:
            files = [open(x, 'r') for x in self._files]

            while True:
                lines = [line_to_data(f.readline()) for f in files]
                min_so_far = None

                # pick min so far
                for i, data in enumerate(lines):
                    min_so_far = i if (min_so_far is None and data) else min_so_far if (min_so_far is not None and lines[min_so_far].time < data.time) else i if data else None

                if min_so_far is None:
                    # done
                    break

                # tick with data
                self.receive(lines[min_so_far])

                # increment that data
                lines[min_so_far] = line_to_data(files[min_so_far].readline())

                if not lines[min_so_far]:
                    # out of data
                    files[min_so_far].close()

        log.info('Backtest done, running analysis.')

        self.callback(TickType.ANALYZE, None)

        log.info('Analysis completed.')

    def receive(self, data: MarketData) -> None:
        # TODO allow if market data for bid/ask
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
