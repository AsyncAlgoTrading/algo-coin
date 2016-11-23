from config import ExchangeConfig
from data_source import StreamingDataSource
from structs import MarketData


class Exchange(StreamingDataSource):
    def __init__(self, options: ExchangeConfig):
        super(Exchange, self).__init__(options)

    def _callback(self, field: str, data: MarketData):
        for cb in self._callbacks[field]:
            cb(data)
