import requests
try:
    from algo_coin.util import insertPythonTime
except Exception:
    from util import insertPythonTime


class CoinbaseExchange(object):
    def __init__(self):
        self.api_url = 'http://api.exchange.coinbase.com/'

    def _call(self, method, params={}):
        url = {
            'products': 'products',
            'order_book': 'products/BTC-USD/book',
            'product_ticker': 'products/BTC-USD/ticker',
            'product_trades': 'products/BTC-USD/trades',
            'product_stats': 'products/BTC-USD/stats',
            'currencies': 'currencies/',
            'time': 'time/'
        }

        return insertPythonTime(requests.get(self.api_url +
                                url[method], params=params).json())

    def getProducts(self):
        return self._call("products")

    def getProductOrderBook(self, level=1):
        return self._call("order_book", {'level': level})

    def getProductTicker(self):
        return self._call("product_ticker")

    def getProductTrades(self):
        return self._call("product_trades")

    def getProductHistoricRates(self):
        raise Exception("not implemented yet")

    def getProductStats(self):
        return self._call("product_stats")

    def getCurrencies(self):
        return self._call("currencies")

    def getTime(self):
        return self._call("time")
